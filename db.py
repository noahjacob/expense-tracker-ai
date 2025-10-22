import os
import sqlite3

DB_PATH = os.getenv("DB_PATH", "expenses.db")

# Get absolute path for logging
absolute_db_path = os.path.abspath(DB_PATH)
print(f"📁 Database file: {absolute_db_path}")

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    schema = """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sw_expense_id INTEGER UNIQUE,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT,
        source TEXT DEFAULT 'personal',
        date TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_conn() as conn:
        conn.executescript(schema)

def add_personal_expense(description: str, amount: float, category: str = None):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO expenses (description, amount, category, source) VALUES (?, ?, ?, 'personal')",
            (description, amount, category)
        )
        conn.commit()

def list_expenses(limit=10):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, description, amount, category, source, date FROM expenses ORDER BY date DESC LIMIT ?",
            (limit,)
        )
        return cur.fetchall()
    
def add_splitwise_expense(sw_id: int, description: str, amount: float, category: str = None, date: str = None):
    """Insert a Splitwise expense row into DB (ignores duplicates)."""
    with get_conn() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO expenses (sw_expense_id, description, amount, category, source, date)
            VALUES (?, ?, ?, ?, 'splitwise', ?)
            """,
            (sw_id, description, amount, category, date),
        )
        conn.commit()

def query_db(sql: str):
    sql_lower = sql.strip().lower()
    print(sql_lower)
    if not sql_lower.startswith("select"):
        return [{"error": "Only SELECT queries are allowed"}]

    forbidden = ["insert", "update", "delete", "drop", "alter", "pragma"]
    if any(word in sql_lower for word in forbidden):
        return [{"error": "Unsafe query detected"}]

    # 🟡 Patch: make category comparisons case-insensitive
    if "where category =" in sql_lower:
        sql = sql.replace("WHERE category =", "WHERE LOWER(category) = LOWER")

    with get_conn() as con:
        print("SQL", sql)
        cur = con.execute(sql)
        raw_rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        rows = [dict(zip(columns, r)) for r in raw_rows]

    if not rows:
        return "No results found."

    return rows

def get_spending_by_category(period: str = "month"):
    """Get spending grouped by category for a given period."""
    period_map = {
        "week": "-7 days",
        "month": "start of month",
        "year": "start of year"
    }
    
    period_filter = period_map.get(period, "start of month")
    
    sql = f"""
    SELECT category, SUM(amount) as total, COUNT(*) as count
    FROM expenses 
    WHERE date >= date('now', '{period_filter}')
    GROUP BY category 
    ORDER BY total DESC
    """
    
    with get_conn() as con:
        cur = con.execute(sql)
        raw_rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        rows = [dict(zip(columns, r)) for r in raw_rows]
    
    return rows

def get_monthly_comparison(period1: str = "this_month", period2: str = "last_month"):
    """Compare spending between two periods."""
    period_sql = {
        "this_month": "strftime('%Y-%m', date) = strftime('%Y-%m', 'now')",
        "last_month": "strftime('%Y-%m', date) = strftime('%Y-%m', 'now', '-1 month')",
        "this_year": "strftime('%Y', date) = strftime('%Y', 'now')",
        "last_year": "strftime('%Y', date) = strftime('%Y', 'now', '-1 year')"
    }
    
    sql1 = f"SELECT SUM(amount) as total FROM expenses WHERE {period_sql.get(period1, period_sql['this_month'])}"
    sql2 = f"SELECT SUM(amount) as total FROM expenses WHERE {period_sql.get(period2, period_sql['last_month'])}"
    
    with get_conn() as con:
        cur1 = con.execute(sql1)
        total1 = cur1.fetchone()[0] or 0
        
        cur2 = con.execute(sql2)
        total2 = cur2.fetchone()[0] or 0
    
    if total2 > 0:
        change_pct = ((total1 - total2) / total2) * 100
    else:
        change_pct = 0
    
    return {
        "period1": period1,
        "period2": period2,
        "total1": total1,
        "total2": total2,
        "change": total1 - total2,
        "change_percent": change_pct,
        "summary": f"{period1}: ${total1:.2f}, {period2}: ${total2:.2f}, Change: {change_pct:+.1f}%"
    }

def get_spending_trends(period: str = "month"):
    """Get spending trends over the specified period."""
    try:
        if period == "week":
            sql = """
            SELECT date(date) as day, SUM(amount) as total
            FROM expenses
            WHERE date >= date('now', '-7 days')
            GROUP BY date(date)
            ORDER BY day DESC
            """
        elif period == "year":
            sql = """
            SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
            FROM expenses
            WHERE date >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month DESC
            """
        else:  # month
            sql = """
            SELECT strftime('%Y-%m-%d', date) as day, SUM(amount) as total
            FROM expenses
            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
            GROUP BY strftime('%Y-%m-%d', date)
            ORDER BY day DESC
            LIMIT 10
            """
        
        with get_conn() as con:
            cur = con.execute(sql)
            raw_rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            rows = [dict(zip(columns, r)) for r in raw_rows]
        
        if not rows:
            return f"No spending data found for the {period} period. Try adding some expenses first!"
        
        # Format output
        total = sum(r['total'] for r in rows if r['total'])
        avg = total / len(rows) if rows else 0
        
        result = f"Spending trends ({period}):\n"
        result += f"Total: ${total:.2f}, Average: ${avg:.2f}/day\n"
        result += "Recent activity:\n"
        for r in rows[:5]:
            day_val = r.get('day') or r.get('month', 'Unknown')
            amount = r.get('total', 0)
            result += f"  {day_val}: ${amount:.2f}\n"
        
        return result
    except Exception as e:
        return f"Error analyzing spending trends: {str(e)}"

def get_category_breakdown():
    """Get category breakdown with percentages for current month."""
    try:
        sql = """
        SELECT 
            category,
            SUM(amount) as total,
            COUNT(*) as count
        FROM expenses
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        GROUP BY category
        ORDER BY total DESC
        """
        
        with get_conn() as con:
            cur = con.execute(sql)
            raw_rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            rows = [dict(zip(columns, r)) for r in raw_rows]
        
        if not rows:
            return "No expenses found for this month. Add some expenses to see the breakdown!"
        
        total = sum(r['total'] for r in rows if r['total'])
        
        result = f"Category Breakdown (This Month - Total: ${total:.2f}):\n"
        for r in rows:
            pct = (r['total'] / total * 100) if total > 0 else 0
            cat_name = r['category'] or 'Uncategorized'
            result += f"  {cat_name}: ${r['total']:.2f} ({pct:.1f}%) - {r['count']} transactions\n"
        
        return result
    except Exception as e:
        return f"Error analyzing categories: {str(e)}"

if __name__ == "__main__":
    init_db()
    print("Database ready.")
