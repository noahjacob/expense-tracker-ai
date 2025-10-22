from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import agent
from db import init_db, query_db
from sync_splitwise import sync_expenses

app = FastAPI(title="Expense Tracker API")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Helper functions to parse tool results
def parse_query_result(content: str):
    """Parse SQL query results into structured data"""
    if not content or "No results" in content or "Error" in content:
        return None, None
    
    # Check if it's a multi-row result (contains |)
    if " | " in content:
        lines = content.strip().split("\n")
        rows = []
        headers = set()
        
        # Try to detect if it's an expense list
        is_expense_list = False
        for line in lines[:10]:  # Limit to 10 rows
            parts = line.split(" | ")
            row_dict = {}
            for part in parts:
                if ": " in part:
                    key, val = part.split(": ", 1)
                    row_dict[key] = val
                    headers.add(key)
                    if key.lower() in ["description", "amount", "category", "date"]:
                        is_expense_list = True
            if row_dict:
                rows.append(row_dict)
        
        if rows:
            if is_expense_list:
                # Format as list for better visualization
                items = []
                for row in rows:
                    items.append({
                        "description": row.get("description", ""),
                        "amount": row.get("amount", "0"),
                        "category": row.get("category", ""),
                        "date": row.get("date", "")
                    })
                return {"items": items}, "list"
            else:
                return {
                    "headers": list(headers),
                    "rows": rows
                }, "table"
    
    # Single value or simple text
    return {"text": content}, "text"

def parse_insights_result(content: str):
    """Parse spending insights into structured data"""
    if not content or "Error" in content:
        return None, None
    
    sections = []
    current_section = None
    
    for line in content.split("\n"):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("**") and line.endswith("**"):
            # Section header
            if current_section:
                sections.append(current_section)
            current_section = {"title": line.strip("*").strip(), "items": []}
        elif line.startswith("•"):
            # List item
            if current_section:
                current_section["items"].append(line[1:].strip())
        elif current_section and not line.startswith("📊"):
            # Regular content
            if "items" not in current_section:
                current_section["items"] = []
            current_section["content"] = line
    
    if current_section:
        sections.append(current_section)
    
    if sections:
        return {"sections": sections}, "insights"
    
    return {"text": content}, "text"

# Models
init_db()

# Models
class ChatMessage(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    response: str
    data: Optional[dict] = None  # Structured data for visualization
    data_type: Optional[str] = None  # 'table', 'list', 'insights', 'text'
    
class ExpenseOverview(BaseModel):
    total: float
    count: int
    top_categories: List[dict]

# In-memory conversation state (replace with Redis/DB for production)
conversation_state = {"messages": []}

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Expense Tracker API"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat with the expense agent"""
    global conversation_state
    
    try:
        # Invoke agent with message
        conversation_state = agent.invoke(
            conversation_state | {"messages": [{"role": "user", "content": message.message}]},
            config={"recursion_limit": 50}
        )
        
        # Get last message
        last_msg = conversation_state["messages"][-1]
        reply = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
        
        # Ensure reply is a string
        if not isinstance(reply, str):
            reply = str(reply)
        
        # Extract structured data from tool calls
        structured_data = None
        data_type = None
        
        # Check if any tools were called and extract their results
        for msg in conversation_state["messages"][-5:]:  # Check last 5 messages
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_name = tool_call.get("name") if isinstance(tool_call, dict) else getattr(tool_call, "name", None)
                    
                    # Find the tool result message
                    tool_result_idx = conversation_state["messages"].index(msg) + 1
                    if tool_result_idx < len(conversation_state["messages"]):
                        tool_result_msg = conversation_state["messages"][tool_result_idx]
                        
                        if hasattr(tool_result_msg, "content"):
                            result_content = tool_result_msg.content
                            
                            # Log the raw tool result
                            print(f"🔍 Tool: {tool_name}")
                            print(f"🔍 Raw result: {result_content[:500]}...")  # First 500 chars
                            
                            # Parse result based on tool type
                            if tool_name == "run_query":
                                structured_data, data_type = parse_query_result(result_content)
                                print(f"🔍 Parsed data type: {data_type}")
                                if structured_data:
                                    print(f"🔍 Parsed data keys: {structured_data.keys()}")
                            elif tool_name == "get_spending_insights":
                                structured_data, data_type = parse_insights_result(result_content)
        
        # Log final response
        print(f"🔍 Final reply length: {len(reply)}")
        print(f"🔍 Reply preview: {reply[:200]}...")
        print(f"🔍 Structured data type: {data_type}")
        
        return ChatResponse(response=reply, data=structured_data, data_type=data_type)
    except Exception as e:
        error_msg = str(e)
        
        # Check for rate limit
        if "rate_limit" in error_msg.lower() or "429" in error_msg:
            return ChatResponse(
                response="⚠️ Groq rate limit reached (100k tokens/day). Try again tomorrow or upgrade your API key. For now, you can still view your expenses in the Recent Expenses section below!"
            )
        
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Chat error: {error_details}")
        return ChatResponse(response=f"❌ Error: {error_msg}")

@app.post("/clear-conversation")
async def clear_conversation():
    """Clear conversation state"""
    global conversation_state
    
    conversation_state = {"messages": []}
    
    return {"status": "ok", "message": "Conversation cleared"}

@app.get("/overview", response_model=ExpenseOverview)
async def get_overview():
    """Get expense overview for current month"""
    try:
        print("🔍 /overview endpoint called")
        
        # Total this month
        total_result = query_db(
            "SELECT SUM(amount) as total FROM expenses WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')"
        )
        print(f"🔍 Total query result: {total_result}")
        total = total_result[0]['total'] if total_result and total_result[0]['total'] else 0
        print(f"🔍 Total: ${total}")
        
        # Count
        count_result = query_db(
            "SELECT COUNT(*) as count FROM expenses WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')"
        )
        print(f"🔍 Count query result: {count_result}")
        count = count_result[0]['count'] if count_result else 0
        print(f"🔍 Count: {count}")
        
        # Top categories
        categories = query_db("""
            SELECT category, SUM(amount) as total, COUNT(*) as count 
            FROM expenses 
            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
            GROUP BY category 
            ORDER BY total DESC 
            LIMIT 5
        """)
        print(f"🔍 Categories: {categories}")
        
        top_categories = [
            {
                "category": row['category'],
                "total": float(row['total']),
                "count": row['count']
            }
            for row in (categories or [])
        ]
        
        return ExpenseOverview(
            total=float(total),
            count=count,
            top_categories=top_categories
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync-splitwise")
async def sync_splitwise():
    """Sync expenses from Splitwise"""
    try:
        if not os.getenv("SPLITWISE_ACCESS_TOKEN"):
            raise HTTPException(status_code=400, detail="Splitwise not configured")
        
        sync_expenses(limit=10)
        return {"status": "success", "message": "Synced successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/expenses")
async def get_expenses(limit: int = 50):
    """Get recent expenses"""
    try:
        expenses = query_db(f"""
            SELECT id, description, amount, category, date, source
            FROM expenses 
            ORDER BY date DESC 
            LIMIT {limit}
        """)
        
        return [dict(row) for row in (expenses or [])]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Expense Tracker API...")
    print("📝 API will be available at http://localhost:8000")
    print("📖 Docs at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
