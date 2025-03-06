import os
import requests
from dotenv import load_dotenv

load_dotenv()
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
if not APOLLO_API_KEY:
    raise ValueError("APOLLO_API_KEY environment variable is not set")

# Base URL for Apollo API endpoints
APOLLO_BASE_URL = "https://api.apollo.io/api/v1"

# Apollo List IDs
CHATGPT_MANUFACTURING_US_LIST_ID = "67a02758363e7e0021d20006"
LA_SMALL_BUSINESS_LIST_ID = "67b4bbdca0e52a00219a0e35"

# Set the current list ID and name
CURRENT_LIST_ID = LA_SMALL_BUSINESS_LIST_ID
CURRENT_LIST_NAME = "la_small_business"  # This will be used as the directory name

def get_contacts_from_apollo(per_page=100):
    """
    Retrieves a list of contacts from a specific Apollo list by searching for contacts.
    Filters by a specific list ID and extracts website and additional fields.
    Skips the first 60 contacts.
    
    :param per_page: Number of contacts to retrieve per API call.
    :return: A list of dictionaries, each with keys:
             'website', 'first_name', 'last_name', 'email', 'location'
    """
    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": APOLLO_API_KEY
    }
    
    url = f"{APOLLO_BASE_URL}/contacts/search"
    
    # Change page number to 11 since you want that page
    payload = {
        "page": 15,  # Changed from 10 to 11
        "per_page": per_page,
        "label_ids": [CURRENT_LIST_ID]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching contacts: {e}")
        return []
    
    data = response.json()
    contacts = data.get("contacts", [])
    results = []
    
    for contact in contacts:
        # Extract website URL from the contact or nested account/organization fields.
        website = contact.get("website_url")
        company_name = None
        if not website:
            account = contact.get("account", {})
            organization = contact.get("organization", {})
            website = account.get("website_url") or organization.get("website_url")
            company_name = account.get("name") or organization.get("name")
        if website:
            first_name = contact.get("first_name", "")
            last_name = contact.get("last_name", "")
            email = contact.get("email", "")
            # Compose location from available fields.
            city = contact.get("city", "")
            state = contact.get("state", "")
            country = contact.get("country", "")
            location = ", ".join(filter(None, [city, state, country]))
            results.append({
                "website": website,
                "company_name": company_name,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "location": location
            })
    
    return results

if __name__ == "__main__":
    contacts = get_contacts_from_apollo()
    print(f"Fetched {len(contacts)} contacts from Apollo:")
    for contact in contacts:
        print(contact)
