import os
import logging
import requests
import base64
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = "sandboxa8bc3f5031ff4356aa495c71afc9ab88.mailgun.org"  # Updated to use the working sandbox domain
SENDER_NAME = os.getenv("SENDER_NAME", "Mailgun Sandbox")
SENDER_TITLE = os.getenv("SENDER_TITLE", "Growth Consultant")
SENDER_COMPANY = os.getenv("SENDER_COMPANY", "Angus Design")
SENDER_EMAIL = "postmaster@sandboxa8bc3f5031ff4356aa495c71afc9ab88.mailgun.org"  # Updated to use the authorized sender

def encode_image_to_base64(image_path):
    """
    Encode an image to base64 for embedding in HTML
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64-encoded image data URL
    """
    try:
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
            base64_encoded = base64.b64encode(image_data).decode('utf-8')
            return f"data:image/png;base64,{base64_encoded}"
    except Exception as e:
        logger.error(f"Error encoding image: {e}")
        return None

def send_email(to_email, subject, body_html):
    """
    Send an email using Mailgun API
    
    Args:
        to_email (str): Recipient's email address
        subject (str): Email subject
        body_html (str): Email body in HTML format
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not MAILGUN_API_KEY:
        logger.error("Mailgun API key not found in environment variables")
        return False
    
    domain = MAILGUN_DOMAIN  # Use our hardcoded sandbox domain directly
    
    try:
        logger.info(f"Sending email to: {to_email}")
        
        url = f"https://api.mailgun.net/v3/{domain}/messages"
        auth = ("api", MAILGUN_API_KEY)
        
        data = {
            "from": f"{SENDER_NAME} <{SENDER_EMAIL}>",
            "to": to_email,
            "subject": subject,
            "html": body_html
        }
        
        logger.debug(f"Sending with from: {SENDER_NAME} <{SENDER_EMAIL}>")
        logger.debug(f"Using domain: {domain}")
        
        response = requests.post(url, auth=auth, data=data)
        
        # Log the response for debugging
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response text: {response.text[:500]}")
        
        response.raise_for_status()
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email through Mailgun: {e}")
        return False

def send_emails_through_mailgun(successful_contacts):
    """
    Send emails using Mailgun API
    
    Args:
        successful_contacts (list): List of dictionaries with contact and email content info
        
    Returns:
        bool: True if emails were sent successfully, False otherwise
    """
    if not successful_contacts:
        logger.error("No contacts to send emails to")
        return False
    
    if not MAILGUN_API_KEY:
        logger.error("Mailgun API key not found in environment variables")
        return False
    
    logger.info(f"Preparing to send emails to {len(successful_contacts)} contacts through Mailgun")
    
    # Track successes and failures
    successes = 0
    failures = 0
    
    # Process each contact
    for i, contact_data in enumerate(successful_contacts, 1):
        contact = contact_data["contact"]
        email = contact.get("email", "")
        
        if not email:
            logger.warning(f"Contact {i} missing email, skipping")
            failures += 1
            continue
        
        logger.info(f"Processing contact {i}/{len(successful_contacts)}: {email}")
        
        try:
            # Instead of uploading to Mailgun, we'll use the image directly in base64 format
            # The image is already encoded in base64 in the HTML
            logger.info(f"Using base64 encoded image in email")
            
            # Send email through Mailgun
            result = send_email(email, contact_data["subject"], contact_data["body_html"])
            
            if result:
                logger.info(f"Successfully sent email to: {email}")
                successes += 1
            else:
                logger.error(f"Failed to send email to: {email}")
                failures += 1
                
        except Exception as e:
            logger.error(f"Error sending email to {email}: {e}")
            failures += 1
    
    # Summary
    logger.info(f"Email sending complete. Successes: {successes}, Failures: {failures}")
    return successes > 0 