import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://secure.splitwise.com/api/v3.0"
TOKEN = os.getenv("SPLITWISE_ACCESS_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def get_expenses(limit=5):
    """Fetch recent Splitwise expenses"""
    r = requests.get(f"{BASE_URL}/get_expenses?limit={limit}", headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_group(group_id):
    """Fetch group details by ID"""
    r = requests.get(f"{BASE_URL}/get_group/{group_id}", headers=HEADERS)
    r.raise_for_status()
    return r.json()