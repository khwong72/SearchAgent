import os
import sys
import time
import logging
from dotenv import load_dotenv
sys.path.append("..") # Add parent directory to path to import apollo
from apollo import get_contacts_from_apollo
from semrush_capture import capture_semrush_report
from apollo_sender import upload_image_to_apollo, create_email_template, start_email_sequence
from email_preparer import prepare_email_template

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    # Check if we have all required environment variables
    required_vars = ["APOLLO_API_KEY", "OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    # Get command line arguments for number of contacts
    if len(sys.argv) != 2:
        logger.error("Usage: python3 main.py <number_of_contacts>")
        sys.exit(1)
    
    try:
        num_contacts = int(sys.argv[1])
    except ValueError:
        logger.error("Please provide a valid number for contacts to process")
        sys.exit(1)
    
    # Create output directory
    reports_dir = "semrush_reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    # Get contacts from Apollo
    logger.info(f"Fetching {num_contacts} contacts from Apollo")
    contacts = get_contacts_from_apollo()
    if not contacts:
        logger.error("No contacts retrieved from Apollo")
        sys.exit(1)
    
    logger.info(f"Retrieved {len(contacts)} contacts, processing first {num_contacts}")
    contacts = contacts[:num_contacts]
    
    # Process each contact
    successful_contacts = []
    contact_ids = []
    
    for i, contact in enumerate(contacts, 1):
        website = contact.get("website", "")
        if not website:
            logger.warning(f"Contact {i} has no website, skipping")
            continue
        
        logger.info(f"Processing contact {i}/{num_contacts}: {contact.get('first_name', '')} {contact.get('last_name', '')} - {website}")
        
        # Capture SEMRush report
        report_path = capture_semrush_report(website, reports_dir)
        if not report_path:
            logger.warning(f"Failed to capture SEMRush report for {website}, skipping")
            continue
        
        # Upload image to Apollo
        image_url = upload_image_to_apollo(report_path)
        if not image_url:
            logger.warning(f"Failed to upload image for {website}, skipping")
            continue
        
        # Prepare email content
        subject, body_html = prepare_email_template(contact, image_url)
        
        # Add to successful contacts list
        successful_contacts.append({
            "contact": contact,
            "image_url": image_url,
            "subject": subject,
            "body_html": body_html
        })
        
        contact_ids.append(contact.get("id"))
        
        # Sleep briefly to avoid overloading APIs
        time.sleep(1)
    
    # If we have successful contacts, create email template and start sequence
    if successful_contacts:
        logger.info(f"Successfully processed {len(successful_contacts)} contacts")
        
        # Create a template for the first contact (same template will be used for all)
        template_name = f"SEMRush Analysis {time.strftime('%Y-%m-%d')}"
        template_id = create_email_template(
            template_name,
            successful_contacts[0]["subject"],
            successful_contacts[0]["body_html"]
        )
        
        if template_id:
            # Start email sequence
            sequence_result = start_email_sequence(contact_ids, template_id)
            if sequence_result:
                logger.info(f"Email sequence started successfully for {len(contact_ids)} contacts")
            else:
                logger.error("Failed to start email sequence")
        else:
            logger.error("Failed to create email template")
    else:
        logger.warning("No contacts were successfully processed")

if __name__ == "__main__":
    main() 