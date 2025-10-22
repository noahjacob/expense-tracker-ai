import os
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from db import add_personal_expense, query_db
from dotenv import load_dotenv
from sync_splitwise import sync_expenses

load_dotenv()

# Ollama setup - runs locally, unlimited usage!
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct-q4_K_M")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

print(f"🦙 Using Ollama (Local): {OLLAMA_MODEL}")
print(f"📍 Ollama server: {OLLAMA_BASE_URL}")

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)

# Simple tools - just the essentials
@tool
def add_expense(description: str, amount: float, category: str = "General"):
    """Add a new expense to the database.
    
    Args:
        description: What the expense was for
        amount: Amount in dollars (e.g., 25.50)
        category: Optional category (default: General)
    """
    try:
        amount = float(amount)
        add_personal_expense(description, amount, category)
        return f"✅ Added: ${amount:.2f} for {description}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@tool
def run_query(sql: str):
    """Execute a SQL query on the expenses database.
    
    Schema: expenses(id, sw_expense_id, description, amount, category, source, date)
    Date format: 'YYYY-MM-DD'
    
    Example: SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """
    try:
        rows = query_db(sql)
        if not rows:
            return "No results found."
        
        # Single value result
        if len(rows) == 1 and len(rows[0]) == 1:
            key = list(rows[0].keys())[0]
            val = rows[0][key]
            if isinstance(val, (int, float)):
                return f"${float(val):.2f}"
            return str(val)
        
        # Multiple rows - format as text
        result_list = []
        for row in rows[:10]:  # Limit to 10 rows
            result_list.append(" | ".join(f"{k}: {v}" for k, v in row.items()))
        return "\n".join(result_list)
    except Exception as e:
        return f"❌ Query error: {str(e)}"

@tool
def get_spending_insights():
    """Get comprehensive spending insights including comparisons to previous periods.
    Shows this month vs last month, category trends, and spending patterns."""
    try:
        # This month
        this_month = query_db("""
            SELECT SUM(amount) as total 
            FROM expenses 
            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        """)
        this_total = this_month[0]['total'] if this_month and this_month[0]['total'] else 0
        
        # Last month
        last_month = query_db("""
            SELECT SUM(amount) as total 
            FROM expenses 
            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now', '-1 month')
        """)
        last_total = last_month[0]['total'] if last_month and last_month[0]['total'] else 0
        
        # Calculate change
        if last_total > 0:
            change = this_total - last_total
            pct_change = (change / last_total) * 100
            comparison = f"{'↑' if change > 0 else '↓'} ${abs(change):.2f} ({abs(pct_change):.1f}%)"
        else:
            comparison = "No previous data"
        
        # Top categories this month
        top_cats = query_db("""
            SELECT category, SUM(amount) as total, COUNT(*) as count
            FROM expenses 
            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
            GROUP BY category
            ORDER BY total DESC
            LIMIT 5
        """)
        
        # Build report
        report = f"""📊 **Spending Insights**

**This Month:** ${this_total:.2f}
**Last Month:** ${last_total:.2f}
**Change:** {comparison}

**Top Categories This Month:**
"""
        if top_cats:
            for cat in top_cats:
                report += f"\n• {cat['category']}: ${cat['total']:.2f} ({cat['count']} transactions)"
        else:
            report += "\nNo expenses yet this month"
        
        return report
    except Exception as e:
        return f"❌ Error getting insights: {str(e)}"

@tool
def sync_splitwise():
    """Sync expenses from Splitwise to import shared expenses and bills.
    Use this when users want to import or sync their Splitwise data."""
    try:
        count = sync_expenses(limit=50)  # Sync last 50 expenses
        return f"✅ Successfully synced {count} expenses from Splitwise!"
    except Exception as e:
        return f"❌ Error syncing Splitwise: {str(e)}"

tools = [add_expense, run_query, get_spending_insights, sync_splitwise]

SYSTEM_PROMPT = """You are an expense tracking assistant. You have access to a SQLite database of expenses.

When users ask about their spending, use the appropriate tools to get the data and present it clearly.

For month-to-month comparisons, use get_spending_insights.
For specific queries, use run_query.
To add expenses, use add_expense.
To sync/import from Splitwise, use sync_splitwise.

Important: Present the information directly without mentioning which tools or functions you used. 
Just give the user the insights and data they asked for in a natural, conversational way."""

# Create simple agent
agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
