import os
from db import init_db, add_splitwise_expense, list_expenses
from splitwise_client import get_expenses, get_group
from mappers import map_expense_to_row
from dotenv import load_dotenv

load_dotenv()
MY_USER_ID = int(os.getenv("MY_USER_ID"))  # put your ID in .env

# Cache for group names to avoid repeated API calls
group_cache = {}

def sync_expenses(limit=5):
    data = get_expenses(limit=limit)
    expenses = data.get("expenses", [])
    synced_count = 0
    
    for e in expenses:
        # Check if user is in this expense and get their owed share
        user_in_expense = False
        user_owed_share = 0.0
        
        for u in e.get("users", []):
            if u.get("user_id") == MY_USER_ID:
                user_in_expense = True
                user_owed_share = float(u.get("owed_share", 0.0))
                break
        
        # Skip if user is not part of this expense
        if not user_in_expense:
            continue
        
        # Skip if user's share is $0 (they don't owe anything)
        if user_owed_share == 0.0:
            continue
        
        # Get group name if not cached
        group_id = e.get("group_id")
        group_name = None
        
        if group_id:
            if group_id not in group_cache:
                try:
                    group_data = get_group(group_id)
                    group_cache[group_id] = group_data.get("group", {}).get("name", "Unknown")
                except:
                    group_cache[group_id] = "Unknown"
            group_name = group_cache[group_id]
        
        sw_id, desc, amount, category, date = map_expense_to_row(e, MY_USER_ID, group_name)
        add_splitwise_expense(sw_id, desc, amount, category, date)
        synced_count += 1
    
    print(f"✅ Synced {synced_count} expenses into DB.")
    return synced_count  # Return count for the agent tool

if __name__ == "__main__":
    init_db()
    sync_expenses(limit=5)
    print("🔎 Checking DB contents:")
    rows = list_expenses(5)
    for row in rows:
        print(row)