import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
APOLLO_BASE_URL = "https://api.apollo.io/api/v1"
LA_SMALL_BUSINESS_LIST_ID = "67b4bbdca0e52a00219a0e35"

def test_apollo_pages():
    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": APOLLO_API_KEY
    }
    
    url = f"{APOLLO_BASE_URL}/contacts/search"
    
    # Test first page to get total count
    payload = {
        "page": 1,
        "per_page": 100,
        "label_ids": [LA_SMALL_BUSINESS_LIST_ID]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        total_contacts = data.get("pagination", {}).get("total_entries", 0)
        total_pages = data.get("pagination", {}).get("total_pages", 0)
        current_page_contacts = len(data.get("contacts", []))
        
        print(f"Total contacts in list: {total_contacts}")
        print(f"Total pages: {total_pages}")
        print(f"Contacts on current page: {current_page_contacts}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_apollo_pages() 