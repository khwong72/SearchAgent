import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_simple_message():
    api_key = os.getenv('MAILGUN_API_KEY')
    if not api_key:
        print("MAILGUN_API_KEY not found in environment variables")
        return None
        
    print(f"Using API key: {api_key[:5]}...")
    
    return requests.post(
        "https://api.mailgun.net/v3/sandboxa8bc3f5031ff4356aa495c71afc9ab88.mailgun.org/messages",
        auth=("api", api_key),
        data={"from": "Mailgun Sandbox <postmaster@sandboxa8bc3f5031ff4356aa495c71afc9ab88.mailgun.org>",
            "to": "Peter Wong <peter@constellarlabs.co>",  # Updated to use your verified email
            "subject": "Hello Peter Wong",
            "text": "Congratulations Peter Wong, you just sent an email with Mailgun! You are truly awesome!"})

if __name__ == "__main__":
    print("Sending test email...")
    response = send_simple_message()
    if response:
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.text}")
    else:
        print("Failed to send email") 