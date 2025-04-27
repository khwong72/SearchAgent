import os
import sys
import csv
import base64
import logging
from dotenv import load_dotenv
from email_preparer import prepare_email_template
from mailgun_sender import send_emails_through_mailgun

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def read_contacts_from_csv(csv_file):
    """Read contact information from a CSV file"""
    contacts = []
    
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                contacts.append(row)
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        return []
    
    return contacts

def encode_image_to_base64(image_path):
    """Encode an image to base64 for embedding in HTML"""
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
        logger.error("Usage: python3 simple_workflow_test.py <path_to_csv_file> [test_image]")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    # Use a sample test image if provided, otherwise use a placeholder
    test_image = "semrush_reports/test_image.png"
    if len(sys.argv) > 2:
        test_image = sys.argv[2]
    
    # Check if test image exists
    if not os.path.exists(test_image):
        logger.error(f"Test image not found: {test_image}")
        logger.info("Creating sample directories to ensure proper structure")
        os.makedirs("semrush_reports", exist_ok=True)
        os.makedirs("email_previews", exist_ok=True)
        logger.error("Please provide a valid test image path")
        sys.exit(1)
    
    # Read contacts from CSV
    logger.info(f"Reading contacts from {csv_file}")
    contacts = read_contacts_from_csv(csv_file)
    
    if not contacts:
        logger.error("No contacts found in CSV file")
        sys.exit(1)
    
    logger.info(f"Processing {len(contacts)} contacts")
    
    # Process each contact
    successful_contacts = []
    
    for i, contact in enumerate(contacts, 1):
        email = contact.get("email", "")
        website = contact.get("website", "")
        
        logger.info(f"Processing contact {i}/{len(contacts)}: {email} - {website}")
        
        # Encode the test image to base64
        image_data_url = encode_image_to_base64(test_image)
        if not image_data_url:
            logger.warning(f"Failed to encode test image, skipping contact: {email}")
            continue
        
        # Prepare email content
        logger.info(f"Preparing email content for {email}")
        subject, body_html = prepare_email_template(contact, image_data_url)
        
        # Save the HTML email for review
        email_output_dir = "email_previews"
        os.makedirs(email_output_dir, exist_ok=True)
        email_file = os.path.join(email_output_dir, f"email_{i}_{website.replace('/', '_').replace(':', '_')}.html")
        
        with open(email_file, 'w', encoding='utf-8') as f:
            f.write(body_html)
        
        logger.info(f"Email preview saved to {email_file}")
        
        # Add to successful contacts list
        successful_contacts.append({
            "contact": contact,
            "image_path": test_image,
            "subject": subject,
            "body_html": body_html
        })
    
    # Send emails
    if successful_contacts:
        logger.info("Sending emails through Mailgun...")
        result = send_emails_through_mailgun(successful_contacts)
        if result:
            logger.info("Emails sent successfully!")
        else:
            logger.error("Failed to send emails through Mailgun. Check logs for details.")
    else:
        logger.warning("No successful contacts to send emails to")

if __name__ == "__main__":
    main() 