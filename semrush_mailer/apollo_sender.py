import os
import logging
import requests
import time
import json
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
APOLLO_BASE_URL = "https://api.apollo.io/v1"

def upload_image_to_apollo(image_path):
    """
    Uploads an image to Apollo for use in email templates
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        str: URL of the uploaded image or None if upload failed
    """
    logger.info(f"Uploading image to Apollo: {image_path}")
    
    if not APOLLO_API_KEY:
        logger.error("APOLLO_API_KEY environment variable is not set")
        return None
    
    if not os.path.exists(image_path):
        logger.error(f"Image file not found: {image_path}")
        return None
    
    # The correct endpoint for Apollo file uploads
    url = f"{APOLLO_BASE_URL}/uploads"  # Changed from /file_uploads to /uploads
    
    headers = {
        "Accept": "application/json",
        "X-Api-Key": APOLLO_API_KEY
    }
    
    try:
        # Log file size and type for debugging
        file_size = os.path.getsize(image_path)
        logger.info(f"File size: {file_size} bytes")
        
        with open(image_path, 'rb') as file:
            files = {'file': file}
            logger.debug(f"Sending POST request to {url}")
            
            response = requests.post(url, headers=headers, files=files)
            
            # Log the response for debugging
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")
            
            try:
                logger.debug(f"Response content: {response.text[:500]}...")
            except:
                logger.debug("Could not log response content")
            
            response.raise_for_status()
            
            data = response.json()
            if 'url' in data:
                logger.info(f"Image uploaded successfully, URL: {data['url']}")
                return data['url']
            else:
                logger.error(f"Unexpected response format: {data}")
                return None
                
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error uploading image to Apollo: {e}")
        
        # Try alternate endpoint if first one fails
        try:
            alternate_url = f"{APOLLO_BASE_URL}/file_upload"  # Try singular endpoint
            logger.info(f"Trying alternate endpoint: {alternate_url}")
            
            with open(image_path, 'rb') as file:
                files = {'file': file}
                alt_response = requests.post(alternate_url, headers=headers, files=files)
                
                logger.debug(f"Alt response status code: {alt_response.status_code}")
                
                alt_response.raise_for_status()
                
                alt_data = alt_response.json()
                if 'url' in alt_data:
                    logger.info(f"Image uploaded successfully with alternate endpoint, URL: {alt_data['url']}")
                    return alt_data['url']
                else:
                    logger.error(f"Unexpected response format from alternate endpoint: {alt_data}")
                    return None
        except Exception as alt_e:
            logger.error(f"Also failed with alternate endpoint: {alt_e}")
            return None
    
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON response: {e}")
        logger.error(f"Response text: {response.text[:500]}...")
        return None
    except Exception as e:
        logger.error(f"Unexpected error uploading image to Apollo: {e}")
        return None

def use_embedded_image(email_html_with_embedded_image):
    """
    Alternative approach: Use the base64-encoded image directly in the email
    
    Args:
        email_html_with_embedded_image (str): Email HTML with base64-encoded image
        
    Returns:
        bool: True, since we'll just use the embedded image directly
    """
    # This function just passes through the HTML with embedded images
    # No need to upload to Apollo servers
    logger.info("Using base64-encoded image directly in email")
    return True

def create_email_template(template_name, subject, body):
    """
    Creates a new email template in Apollo
    
    Args:
        template_name (str): Name for the template
        subject (str): Email subject line
        body (str): Email body HTML
    
    Returns:
        str: Template ID if successful, None if failed
    """
    logger.info(f"Creating email template: {template_name}")
    
    if not APOLLO_API_KEY:
        logger.error("APOLLO_API_KEY environment variable is not set")
        return None
    
    url = f"{APOLLO_BASE_URL}/email_templates"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Key": APOLLO_API_KEY
    }
    
    payload = {
        "name": template_name,
        "subject": subject,
        "body_html": body
    }
    
    try:
        logger.debug(f"Sending POST request to {url}")
        logger.debug(f"Email template subject: {subject}")
        logger.debug(f"Email template length: {len(body)} characters")
        
        response = requests.post(url, headers=headers, json=payload)
        
        # Log the response for debugging
        logger.debug(f"Response status code: {response.status_code}")
        
        try:
            logger.debug(f"Response content: {response.text[:500]}...")
        except:
            logger.debug("Could not log response content")
        
        response.raise_for_status()
        
        data = response.json()
        if 'id' in data:
            logger.info(f"Template created successfully, ID: {data['id']}")
            return data['id']
        else:
            logger.error(f"Unexpected response format: {data}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error creating email template: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON response: {e}")
        logger.error(f"Response text: {response.text[:500]}...")
        return None
    except Exception as e:
        logger.error(f"Unexpected error creating email template: {e}")
        return None

def find_or_create_contact(email, first_name, last_name, company_name):
    """
    Find or create a contact in Apollo by email
    
    Args:
        email (str): Contact's email address
        first_name (str): Contact's first name
        last_name (str): Contact's last name
        company_name (str): Contact's company name
    
    Returns:
        str: Contact ID if found or created, None if failed
    """
    if not APOLLO_API_KEY:
        logger.error("APOLLO_API_KEY environment variable is not set")
        return None
    
    # First, search for the contact by email
    search_url = f"{APOLLO_BASE_URL}/contacts/search"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Key": APOLLO_API_KEY
    }
    
    search_payload = {
        "q_organization_domains": [],
        "q_emails": [email],
        "page": 1,
        "per_page": 1
    }
    
    try:
        logger.info(f"Searching for contact with email: {email}")
        response = requests.post(search_url, headers=headers, json=search_payload)
        response.raise_for_status()
        
        data = response.json()
        contacts = data.get("contacts", [])
        
        if contacts:
            contact_id = contacts[0].get("id")
            logger.info(f"Found existing contact with ID: {contact_id}")
            return contact_id
        
        # If contact not found, create a new one
        logger.info(f"Contact not found, creating new contact: {first_name} {last_name}")
        
        create_url = f"{APOLLO_BASE_URL}/contacts"
        
        create_payload = {
            "contact": {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "organization_name": company_name
            }
        }
        
        create_response = requests.post(create_url, headers=headers, json=create_payload)
        create_response.raise_for_status()
        
        create_data = create_response.json()
        if "contact" in create_data and "id" in create_data["contact"]:
            contact_id = create_data["contact"]["id"]
            logger.info(f"Created new contact with ID: {contact_id}")
            return contact_id
        else:
            logger.error(f"Unexpected response format when creating contact: {create_data}")
            return None
        
    except Exception as e:
        logger.error(f"Error finding or creating contact: {e}")
        return None

def start_email_sequence(contact_ids, template_id, sequence_name=None):
    """
    Starts an email sequence for the given contacts using the specified template
    
    Args:
        contact_ids (list): List of Apollo contact IDs
        template_id (str): Apollo email template ID
        sequence_name (str, optional): Name for the sequence
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not sequence_name:
        sequence_name = f"SEMRush Analysis Sequence {time.strftime('%Y-%m-%d')}"
    
    logger.info(f"Starting email sequence for {len(contact_ids)} contacts")
    
    if not APOLLO_API_KEY:
        logger.error("APOLLO_API_KEY environment variable is not set")
        return False
    
    if not contact_ids:
        logger.error("No contact IDs provided")
        return False
    
    if not template_id:
        logger.error("No template ID provided")
        return False
    
    url = f"{APOLLO_BASE_URL}/email_sequences"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Key": APOLLO_API_KEY
    }
    
    payload = {
        "name": sequence_name,
        "contact_ids": contact_ids,
        "steps": [
            {
                "email_template_id": template_id,
                "delay_in_seconds": 0  # Send immediately
            }
        ]
    }
    
    try:
        logger.debug(f"Sending POST request to {url}")
        logger.debug(f"Contact IDs: {contact_ids}")
        logger.debug(f"Template ID: {template_id}")
        
        response = requests.post(url, headers=headers, json=payload)
        
        # Log the response for debugging
        logger.debug(f"Response status code: {response.status_code}")
        
        try:
            logger.debug(f"Response content: {response.text[:500]}...")
        except:
            logger.debug("Could not log response content")
        
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Email sequence started successfully")
        return True
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error starting email sequence: {e}")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON response: {e}")
        logger.error(f"Response text: {response.text[:500]}...")
        return False
    except Exception as e:
        logger.error(f"Unexpected error starting email sequence: {e}")
        return False

def send_single_email(contact_id, subject, body_html):
    """
    Sends a single email to a contact
    
    Args:
        contact_id (str): Apollo contact ID
        subject (str): Email subject
        body_html (str): Email body HTML
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not APOLLO_API_KEY:
        logger.error("APOLLO_API_KEY environment variable is not set")
        return False
    
    url = f"{APOLLO_BASE_URL}/emails"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Key": APOLLO_API_KEY
    }
    
    payload = {
        "contact_id": contact_id,
        "subject": subject,
        "body_html": body_html
    }
    
    try:
        logger.info(f"Sending single email to contact: {contact_id}")
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Email sent successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error sending single email: {e}")
        return False

def send_emails_through_apollo(successful_contacts):
    """
    Send emails through Apollo using the generated content
    
    Args:
        successful_contacts (list): List of dictionaries with contact and email content info
        
    Returns:
        bool: True if emails were sent successfully, False otherwise
    """
    if not successful_contacts:
        logger.error("No contacts to send emails to")
        return False
    
    apollo_api_key = os.getenv("APOLLO_API_KEY")
    if not apollo_api_key:
        logger.error("APOLLO_API_KEY environment variable is not set")
        return False
    
    logger.info(f"Preparing to send emails to {len(successful_contacts)} contacts through Apollo")
    
    # Track successes and failures
    successes = 0
    failures = 0
    
    # Process each contact individually to ensure more reliable delivery
    for i, contact_data in enumerate(successful_contacts, 1):
        contact = contact_data["contact"]
        
        # Make sure we have email, first_name, last_name
        email = contact.get("email", "")
        first_name = contact.get("first_name", "")
        last_name = contact.get("last_name", "")
        company_name = contact.get("company_name", "")
        
        if not email:
            logger.warning(f"Contact {i} missing email, skipping")
            failures += 1
            continue
        
        logger.info(f"Processing contact {i}/{len(successful_contacts)}: {first_name} {last_name} <{email}>")
        
        # Find or create the contact in Apollo
        contact_id = find_or_create_contact(email, first_name, last_name, company_name)
        
        if not contact_id:
            logger.warning(f"Could not find or create contact for {email}, skipping")
            failures += 1
            continue
        
        try:
            # Get the prepared HTML with base64 image from the successful_contacts data
            subject = contact_data["subject"]
            body_html = contact_data["body_html"]
            
            # Send direct email with embedded image
            logger.info(f"Sending direct email with embedded image to: {email}")
            direct_result = send_single_email(contact_id, subject, body_html)
            
            if direct_result:
                logger.info(f"Successfully sent direct email to: {email}")
                successes += 1
            else:
                logger.error(f"Failed to send direct email to: {email}")
                failures += 1
                
        except Exception as e:
            logger.error(f"Error sending email to {email}: {e}")
            failures += 1
    
    # Summary
    logger.info(f"Email sending complete. Successes: {successes}, Failures: {failures}")
    return successes > 0 