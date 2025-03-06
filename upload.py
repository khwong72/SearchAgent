import os
import time
import csv
import requests
from datetime import datetime
import schedule

def upload_contacts_to_sequence():
    # Apollo API configuration
    APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
    if not APOLLO_API_KEY:
        print("Error: APOLLO_API_KEY environment variable not set")
        return
        
    APOLLO_BASE_URL = "https://api.apollo.io/api/v1"
    SEQUENCE_ID = "67b4f0a251700d0020425aa7"  # Updated with your actual sequence ID
    
    # Test if SEQUENCE_ID has been updated
    if SEQUENCE_ID == "YOUR_SEQUENCE_ID":
        print("Error: Please replace SEQUENCE_ID with your actual sequence ID")
        return
    
    # Add test mode to print payload instead of making API call
    TEST_MODE = True  # Set to False for production
    
    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache", 
        "Content-Type": "application/json",
        "x-api-key": APOLLO_API_KEY
    }
    
    # Read contacts from CSV
    contacts = []
    try:
        with open("not_good_websites.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            contacts = list(reader)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
        
    # Upload contacts to sequence
    url = f"{APOLLO_BASE_URL}/sequence_tasks/bulk_create"
    
    for contact in contacts:
        payload = {
            "sequence_id": SEQUENCE_ID,
            "contact_ids": [],  # Will be populated after contact lookup
            "email_addresses": [contact["email"]]
        }
        
        try:
            if TEST_MODE:
                print(f"TEST MODE - Would send payload:")
                print(f"Headers: {headers}")
                print(f"Payload: {payload}")
                print("---")
            else:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
            print(f"Added {contact['email']} to sequence")
            time.sleep(1)  # Rate limiting
        except requests.RequestException as e:
            print(f"Error adding contact {contact['email']}: {e}")

# Replace the scheduling code with a single test run
if __name__ == "__main__":
    print("Running in test mode...")
    upload_contacts_to_sequence()
