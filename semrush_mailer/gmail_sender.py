import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")  # This should be an App Password
SENDER_NAME = os.getenv("SENDER_NAME", "Calvin Beighle")
SENDER_TITLE = os.getenv("SENDER_TITLE", "Growth Consultant")
SENDER_COMPANY = os.getenv("SENDER_COMPANY", "Angus Design")

def send_email(to_email, subject, body_html):
    """
    Send an email using Gmail SMTP
    
    Args:
        to_email (str): Recipient's email address
        subject (str): Email subject
        body_html (str): Email body in HTML format
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not GMAIL_USER or not GMAIL_PASSWORD:
        logger.error("Gmail credentials not found in environment variables")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{SENDER_NAME} <{GMAIL_USER}>"
        msg['To'] = to_email
        
        # Attach HTML content
        msg.attach(MIMEText(body_html, 'html'))
        
        # Connect to Gmail SMTP server
        logger.info(f"Connecting to Gmail SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login
        logger.info(f"Logging in with Gmail account: {GMAIL_USER}")
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        
        # Send email
        logger.info(f"Sending email to: {to_email}")
        server.send_message(msg)
        
        # Close connection
        server.quit()
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def send_emails_through_gmail(successful_contacts):
    """
    Send emails using Gmail SMTP
    
    Args:
        successful_contacts (list): List of dictionaries with contact and email content info
        
    Returns:
        bool: True if emails were sent successfully, False otherwise
    """
    if not successful_contacts:
        logger.error("No contacts to send emails to")
        return False
    
    if not GMAIL_USER or not GMAIL_PASSWORD:
        logger.error("Gmail credentials not found in environment variables")
        return False
    
    logger.info(f"Preparing to send emails to {len(successful_contacts)} contacts through Gmail")
    
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
            # Get the prepared HTML with base64 image
            subject = contact_data["subject"]
            body_html = contact_data["body_html"]
            
            # Send email through Gmail
            result = send_email(email, subject, body_html)
            
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