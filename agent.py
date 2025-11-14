import os
from datetime import datetime
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from db import add_personal_expense, query_db, delete_expense, delete_expenses_by_ids
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
def add_expense(description: str, amount: float, category: str):
    """Add a new expense to the database.
    
    IMPORTANT: You must ask the user to confirm the category before calling this tool.
    Do not infer or assume the category - the user must explicitly state it.
    
    Args:
        description: What the expense was for
        amount: Amount in dollars (e.g., 25.50)
        category: REQUIRED. Must be explicitly confirmed by user. One of: Groceries, Food & Drink, Transportation, Shopping, Entertainment, Bills & Utilities, Healthcare, General
    
    The category parameter should ONLY come from the user's explicit statement, not your inference.
    If you haven't asked the user which category to use, DO NOT call this tool yet - ask them first.
    """
    try:
        # Validate category
        valid_categories = ["Groceries", "Food & Drink", "Transportation", "Shopping", 
                          "Entertainment", "Bills & Utilities", "Healthcare", "General"]
        if category not in valid_categories:
            return f"❌ Invalid category '{category}'. Please use one of: {', '.join(valid_categories)}"
        
        amount = float(amount)
        add_personal_expense(description, amount, category)
        return f"✅ Added: ${amount:.2f} for {description} (Category: {category})"
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
def delete_expense_by_id(expense_id: int):
    """Delete an expense from the database by its ID.
    
    Use this when the user wants to remove or delete a single expense.
    You'll typically need to first query for the expense to get its ID, then delete it.
    
    Args:
        expense_id: The ID of the expense to delete (from the expenses table)
    """
    try:
        success = delete_expense(expense_id)
        if success:
            return f"✅ Deleted expense ID {expense_id}"
        else:
            return f"❌ No expense found with ID {expense_id}"
    except Exception as e:
        return f"❌ Error deleting expense: {str(e)}"

@tool
def delete_multiple_expenses(expense_ids: list):
    """Delete multiple expenses from the database by their IDs.
    
    Use this when the user wants to remove multiple expenses at once.
    First query to find the expenses and get their IDs, then delete them.
    
    Args:
        expense_ids: List of expense IDs to delete (e.g., [1, 2, 3])
    """
    try:
        if not expense_ids:
            return "❌ No expense IDs provided"
        
        count = delete_expenses_by_ids(expense_ids)
        if count > 0:
            return f"✅ Deleted {count} expense(s)"
        else:
            return "❌ No expenses were deleted"
    except Exception as e:
        return f"❌ Error deleting expenses: {str(e)}"

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
def get_spending_trends(period: str):
    """Get spending trends over time with visual graph data.
    
    Use this when users ask about spending patterns, trends, or want to see how spending changed over time.
    
    Args:
        period: Time period for trends. Must be one of: 'week' (last 7 days), 'month' (last 2 months), 'year' (last 12 months)
    """
    try:
        valid_periods = ['week', 'month', 'year']
        if period not in valid_periods:
            return f"❌ Invalid period. Please use: 'week', 'month', or 'year'"
        
        # Query based on period
        if period == "week":
            sql = """
            SELECT date(date) as date, SUM(amount) as amount
            FROM expenses
            WHERE date >= date('now', '-7 days')
            GROUP BY date(date)
            ORDER BY date ASC
            """
            period_label = "Last 7 Days"
        elif period == "year":
            sql = """
            SELECT strftime('%Y-%m', date) as date, SUM(amount) as amount
            FROM expenses
            WHERE date >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', date)
            ORDER BY date ASC
            """
            period_label = "Last 12 Months"
        else:  # month
            sql = """
            SELECT 
                strftime('%Y-%m', date) as date,
                CASE strftime('%m', date)
                    WHEN '01' THEN 'January'
                    WHEN '02' THEN 'February'
                    WHEN '03' THEN 'March'
                    WHEN '04' THEN 'April'
                    WHEN '05' THEN 'May'
                    WHEN '06' THEN 'June'
                    WHEN '07' THEN 'July'
                    WHEN '08' THEN 'August'
                    WHEN '09' THEN 'September'
                    WHEN '10' THEN 'October'
                    WHEN '11' THEN 'November'
                    WHEN '12' THEN 'December'
                END || ' ' || strftime('%Y', date) as month_name,
                SUM(amount) as amount
            FROM expenses
            WHERE strftime('%Y-%m', date) >= strftime('%Y-%m', 'now', '-1 month')
            GROUP BY strftime('%Y-%m', date)
            ORDER BY date ASC
            """
            period_label = "Last 2 Months"
        
        results = query_db(sql)
        
        if not results or results == "No results found.":
            return f"No spending data found for {period_label}"
        
        # Format as JSON for frontend
        import json
        trend_data = {
            "period": period,
            "period_label": period_label,
            "data": []
        }
        
        for row in results:
            # Use month_name if available (for month period), otherwise use date
            display_label = row.get('month_name') or row['date']
            trend_data["data"].append({
                "date": display_label,
                "amount": float(row['amount']) if row['amount'] else 0
            })
        
        # Return as JSON string that frontend can parse
        return f"TREND_DATA:{json.dumps(trend_data)}"
        
    except Exception as e:
        return f"❌ Error getting trends: {str(e)}"

@tool
def get_category_breakdown(period: str = "month", specific_month: str = None, year: int = None):
    """Get spending breakdown by category with pie chart visualization.
    
    Use this when users ask about category breakdown, spending by category, or want to see their spending distribution.
    
    Args:
        period: Time period for breakdown. Options: 'week', 'month' (current month), 'last_month', 'year', 'all', 'specific_month'
        specific_month: When period='specific_month', specify the month name (e.g., 'September', 'October') or month number (1-12)
        year: Optional year for specific_month (defaults to current year if not provided)
    """
    try:
        # Build date filter based on period
        if period == "week":
            date_filter = "WHERE date >= date('now', '-7 days')"
            period_label = "Last 7 Days"
        elif period == "last_month":
            date_filter = "WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now', '-1 month')"
            period_label = "Last Month"
        elif period == "year":
            date_filter = "WHERE date >= date('now', '-12 months')"
            period_label = "Last 12 Months"
        elif period == "all":
            date_filter = ""
            period_label = "All Time"
        elif period == "specific_month" and specific_month:
            # Handle specific month requests
            month_mapping = {
                'january': '01', 'jan': '01',
                'february': '02', 'feb': '02',
                'march': '03', 'mar': '03',
                'april': '04', 'apr': '04',
                'may': '05',
                'june': '06', 'jun': '06',
                'july': '07', 'jul': '07',
                'august': '08', 'aug': '08',
                'september': '09', 'sep': '09', 'sept': '09',
                'october': '10', 'oct': '10',
                'november': '11', 'nov': '11',
                'december': '12', 'dec': '12'
            }
            
            # Convert month name to number
            month_lower = specific_month.lower()
            month_num = month_mapping.get(month_lower, specific_month)
            
            # Ensure month is 2 digits
            if len(month_num) == 1:
                month_num = f'0{month_num}'
            
            # Use current year if not specified
            if not year:
                year = datetime.now().year
            
            date_filter = f"WHERE strftime('%Y-%m', date) = '{year}-{month_num}'"
            period_label = f"{specific_month.capitalize()} {year}"
        else:  # month (default)
            date_filter = "WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')"
            period_label = "This Month"
        
        sql = f"""
        SELECT 
            category,
            SUM(amount) as total,
            COUNT(*) as count
        FROM expenses
        {date_filter}
        GROUP BY category
        ORDER BY total DESC
        """
        
        results = query_db(sql)
        
        if not results or results == "No results found.":
            return f"No spending data found for {period_label}"
        
        # Format as JSON for frontend
        import json
        
        # Calculate total for percentages
        grand_total = sum(float(row['total']) for row in results if row['total'])
        
        category_data = {
            "period_label": period_label,
            "total": grand_total,
            "categories": [
                {
                    "name": row['category'] or 'Uncategorized',
                    "value": float(row['total']) if row['total'] else 0,
                    "count": row['count'],
                    "percentage": (float(row['total']) / grand_total * 100) if grand_total > 0 else 0
                }
                for row in results
            ]
        }
        
        # Return as JSON string that frontend can parse
        return f"CATEGORY_DATA:{json.dumps(category_data)}"
        
    except Exception as e:
        return f"❌ Error getting category breakdown: {str(e)}"

@tool
def sync_splitwise():
    """Sync expenses from Splitwise to import shared expenses and bills.
    Use this when users want to import or sync their Splitwise data."""
    try:
        count = sync_expenses(limit=50)  # Sync last 50 expenses
        return f"✅ Successfully synced {count} expenses from Splitwise!"
    except Exception as e:
        return f"❌ Error syncing Splitwise: {str(e)}"

tools = [add_expense, run_query, delete_expense_by_id, delete_multiple_expenses, get_spending_insights, get_spending_trends, get_category_breakdown, sync_splitwise]

def get_system_prompt():
    """Generate system prompt with current date."""
    today = datetime.now()
    today_str = today.strftime('%Y-%m-%d')
    month_str = today.strftime('%Y-%m')
    date_display = today.strftime('%B %d, %Y')  # e.g., "November 13, 2025"
    
    return f"""You are an expense tracking assistant. You have access to a SQLite database of expenses.

IMPORTANT: Today's date is {date_display} ({today_str}). When writing queries that reference dates:
- Use 'now' or CURRENT_DATE in SQLite for today's date
- For "recently added" or "today" queries, use: WHERE date >= '{today_str}'
- For "this month" queries, use: WHERE strftime('%Y-%m', date) = '{month_str}'
- For "last month" queries, use: WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now', '-1 month')
- NEVER use dates from past years unless specifically asked
- If a query returns no results, explain what date range you checked and suggest alternatives

When users ask about their spending, use the appropriate tools to get the data and present it clearly.

For month-to-month comparisons, use get_spending_insights.
For specific queries, use run_query.
To add expenses, use add_expense.
To delete/remove expenses, use delete_expense_by_id (you'll need to query for the ID first).
To delete multiple expenses at once, use delete_multiple_expenses with a list of IDs.
To see spending trends over time with graphs, use get_spending_trends.
To see category breakdown with pie chart, use get_category_breakdown.
To sync/import from Splitwise, use sync_splitwise.

CRITICAL WORKFLOW FOR TRENDS:
When a user asks about trends, patterns, or "how spending changed":
1. If they don't specify a time period, ASK them: "Would you like to see trends for the last week, month, or year?"
2. Wait for their response
3. Then call get_spending_trends with the period they chose ('week', 'month', or 'year')

CRITICAL WORKFLOW FOR CATEGORY BREAKDOWN:
When a user asks about "categories", "category breakdown", "spending by category", or "what categories":
1. Use get_category_breakdown tool to show a pie chart
2. Pay attention to time period in user's question:
   - "this month" or no period specified → period='month'
   - "last month" → period='last_month'
   - "last week" or "this week" → period='week'
   - "this year" or "last 12 months" → period='year'
   - "all time" or "ever" → period='all'
   - Specific month name like "September", "October", "January" → period='specific_month', specific_month='September'
   - Specific month with year like "September 2024" → period='specific_month', specific_month='September', year=2024

Examples:
- "Show me my spending categories" → get_category_breakdown(period='month')
- "What categories did I spend on last month?" → get_category_breakdown(period='last_month')
- "Category breakdown for this year" → get_category_breakdown(period='year')
- "Show me category breakdown for September" → get_category_breakdown(period='specific_month', specific_month='September')
- "Categories for October 2024" → get_category_breakdown(period='specific_month', specific_month='October', year=2024)

Example:
User: "Show me my spending trends"
You: "I can show you spending trends! Would you like to see the last week, last 2 months, or last 12 months?"
[WAIT for response]
User: "Last 2 months"
You: [call get_spending_trends(period='month')]

CRITICAL WORKFLOW FOR ADDING EXPENSES:
Step 1: User requests to add an expense (e.g., "add $30 for paneer from Costco")
Step 2: YOU MUST ASK which category to use - DO NOT call add_expense yet!
Step 3: Wait for user to respond with category
Step 4: ONLY THEN call add_expense with the user's confirmed category

NEVER skip Step 2, even if the category seems obvious!

Example conversation:
User: "Add $30 for paneer from Costco"
You: "I'll add $30 for paneer from Costco. Which category should I use? (Groceries, Food & Drink, Shopping, General, etc.)"
[STOP HERE - wait for user response]

User: "Groceries"
You: [NOW call add_expense(description="paneer from Costco", amount=30, category="Groceries")]

FOR DELETING EXPENSES:
When a user wants to delete expense(s), first query to find them, show what you found, then delete by ID(s).

DO NOT assume or infer categories. The user must explicitly confirm.
Available categories: Groceries, Food & Drink, Transportation, Shopping, Entertainment, Bills & Utilities, Healthcare, General

Important: Present the information directly without mentioning which tools or functions you used. 
Just give the user the insights and data they asked for in a natural, conversational way.
NEVER show raw SQL queries or tool call details to the user."""

SYSTEM_PROMPT = get_system_prompt()

# Create simple agent
agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
