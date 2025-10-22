# whoami.py
import os, requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://secure.splitwise.com/api/v3.0"
TOKEN = os.getenv("SPLITWISE_ACCESS_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def get_current_user():
    r = requests.get(f"{BASE_URL}/get_current_user", headers=HEADERS)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    me = get_current_user()["user"]
    print("✅ Your Splitwise User Info:")
    print("ID:", me["id"])
    print("Name:", me["first_name"], me.get("last_name", ""))