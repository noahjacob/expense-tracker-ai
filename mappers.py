from datetime import datetime

# Approximate conversion rates (you can update these or use an API)
CURRENCY_TO_USD = {
    "USD": 1.0,
    "INR": 0.012,  # 1 INR ≈ $0.012 USD
    "EUR": 1.08,
    "GBP": 1.27,
    "CAD": 0.73,
}

def normalize_date(iso_str: str) -> str:
    """
    Convert ISO8601 Splitwise date (e.g. '2025-09-22T23:36:37Z')
    into SQLite-friendly format 'YYYY-MM-DD'.
    """
    if not iso_str:
        return None
    # Remove 'Z' and parse
    dt = datetime.fromisoformat(iso_str.replace("Z", ""))
    return dt.strftime("%Y-%m-%d")   # or "%Y-%m-%d %H:%M:%S" if you want time

def map_expense_to_row(e, my_user_id: int, group_name: str = None):
    """Convert Splitwise expense JSON into (sw_id, desc, amount, category, date)."""
    sw_id = e.get("id")
    desc = e.get("description", "No description")
    category = e.get("category", {}).get("name") if e.get("category") else None

    # normalize date
    raw_date = e.get("date")
    date = normalize_date(raw_date)

    # Get currency code
    currency_code = e.get("currency_code", "USD")

    # Default: total cost
    amount = float(e.get("cost", 0.0))

    # Override with my owed share
    for u in e.get("users", []):
        if u.get("user_id") == my_user_id:
            amount = float(u.get("owed_share", 0.0))
            break

    # Convert to USD if needed
    if currency_code != "USD":
        conversion_rate = CURRENCY_TO_USD.get(currency_code, 1.0)
        amount = amount * conversion_rate
        desc = f"{desc} ({currency_code} {amount/conversion_rate:.2f})"  # Show original amount

    # Add group name if provided
    if group_name:
        desc = f"[{group_name}] {desc}"

    return (sw_id, desc, amount, category, date)