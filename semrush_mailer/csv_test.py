import os
import sys
import time
import csv
import base64
import logging

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Starting script...")
logger.info("Importing dependencies...")

try:
    from dotenv import load_dotenv
    logger.info("Successfully imported dotenv")
except Exception as e:
    logger.error(f"Error importing dotenv: {e}")
    sys.exit(1)

try:
    from semrush_capture import capture_semrush_report
    logger.info("Successfully imported semrush_capture")
except Exception as e:
    logger.error(f"Error importing semrush_capture: {e}")
    sys.exit(1)

try:
    from mailgun_sender import send_emails_through_mailgun
    logger.info("Successfully imported mailgun_sender")
except Exception as e:
    logger.error(f"Error importing mailgun_sender: {e}")
    sys.exit(1)

try:
    from email_preparer import prepare_email_template
    logger.info("Successfully imported email_preparer")
except Exception as e:
    logger.error(f"Error importing email_preparer: {e}")
    sys.exit(1)

# Load environment variables
logger.info("Loading environment variables...")
load_dotenv()

def read_contacts_from_csv(csv_file):
    """
    Read contact information from a CSV file
    
    Expected CSV format:
    email,first_name,last_name,company_name,website
    
    Args:
        csv_file (str): Path to the CSV file
        
    Returns:
        list: List of contact dictionaries
    """
    contacts = []
    
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Make sure we have the required fields
                if 'website' not in row or not row['website']:
                    logger.warning(f"Skipping row without website: {row}")
                    continue
                
                contacts.append(row)
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        return []
    
    return contacts

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

def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        logger.error("Usage: python3 csv_test.py <path_to_csv_file> [num_contacts]")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    # Optional limit on number of contacts to process
    num_contacts = None
    if len(sys.argv) > 2:
        try:
            num_contacts = int(sys.argv[2])
        except ValueError:
            logger.error("Number of contacts must be an integer")
            sys.exit(1)
    
    # Create output directory
    reports_dir = "semrush_reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    # Read contacts from CSV
    logger.info(f"Reading contacts from {csv_file}")
    contacts = read_contacts_from_csv(csv_file)
    
    if not contacts:
        logger.error("No valid contacts found in CSV file")
        sys.exit(1)
    
    if num_contacts:
        contacts = contacts[:num_contacts]
        logger.info(f"Processing first {num_contacts} contacts from CSV")
    else:
        logger.info(f"Processing all {len(contacts)} contacts from CSV")
    
    # Process each contact
    successful_contacts = []
    
    for i, contact in enumerate(contacts, 1):
        website = contact.get("website", "")
        logger.info(f"Processing contact {i}/{len(contacts)}: {contact.get('first_name', '')} {contact.get('last_name', '')} - {website}")
        
        # Capture SEMRush report - with visible browser for debugging
        report_path = capture_semrush_report(website, reports_dir, headless=False)
        if not report_path:
            logger.warning(f"Failed to capture SEMRush report for {website}, skipping")
            continue
        
        # Convert the image to base64 for embedding in HTML
        logger.info("Encoding image to base64")
        image_data_url = encode_image_to_base64(report_path)
        if not image_data_url:
            logger.warning(f"Failed to encode image for {website}, skipping")
            continue
        
        # Prepare email content
        logger.info(f"Preparing email content for {contact.get('email', '')}")
        subject, body_html = prepare_email_template(contact, image_data_url)
        
        # Add to successful contacts list
        successful_contacts.append({
            "contact": contact,
            "image_path": report_path,
            "subject": subject,
            "body_html": body_html
        })
        
        # Save the HTML email for review
        email_output_dir = "email_previews"
        os.makedirs(email_output_dir, exist_ok=True)
        email_file = os.path.join(email_output_dir, f"email_{i}_{website.replace('/', '_').replace(':', '_')}.html")
        
        with open(email_file, 'w', encoding='utf-8') as f:
            f.write(body_html)
        
        logger.info(f"Email preview saved to {email_file}")
        
        # Sleep briefly to avoid overloading SEMRush
        time.sleep(1)
    
    # Summary
    logger.info(f"Processed {len(contacts)} contacts")
    logger.info(f"Successfully generated {len(successful_contacts)} email previews")
    logger.info(f"Email previews saved in the 'email_previews' directory")
    logger.info(f"SEMRush reports saved in the '{reports_dir}' directory")
    
    # Automatically send emails without prompting
    if successful_contacts:
        logger.info("Sending emails through Mailgun...")
        result = send_emails_through_mailgun(successful_contacts)
        if result:
            print("Emails sent successfully!")
        else:
            print("Failed to send emails through Mailgun. Check the logs for details.")

if __name__ == "__main__":
    main() 