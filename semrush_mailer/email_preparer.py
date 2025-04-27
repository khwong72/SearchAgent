import os
import logging
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Jinja2 environment
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
os.makedirs(template_dir, exist_ok=True)
env = Environment(loader=FileSystemLoader(template_dir))

# Create default email template if it doesn't exist
default_template_path = os.path.join(template_dir, 'default_email.html')
if not os.path.exists(default_template_path):
    with open(default_template_path, 'w') as f:
        f.write('''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; }
                .semrush-report { margin: 20px 0; }
                .cta-button { 
                    display: inline-block; 
                    padding: 10px 20px; 
                    background-color: #4CAF50; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 4px; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <p>Hi {{first_name}},</p>
                
                <p>I was reviewing {{company_name}}'s website and thought you might be interested in this SEMRush report on your current online presence:</p>
                
                <div class="semrush-report">
                    <img src="{{semrush_image_url}}" alt="SEMRush report for {{company_name}}" width="100%">
                </div>
                
                <p>I noticed some opportunities for improvement that could help increase your visibility and drive more targeted traffic to your website.</p>
                
                <p>Would you be interested in a brief call to discuss how we could help improve these metrics?</p>
                
                <p>
                    <a href="https://calendly.com/wong-peter/catchup" class="cta-button">Book a 15-min call</a>
                </p>
                
                <p>Best regards,<br>
                {{sender_name}}<br>
                {{sender_title}}<br>
                {{sender_company}}</p>
            </div>
        </body>
        </html>
        ''')

def prepare_email_template(contact_info, semrush_image_url, template_path=None):
    """
    Prepares an email using a template and contact information
    
    Args:
        contact_info (dict): Contact information (name, company, etc.)
        semrush_image_url (str): URL of the uploaded SEMRush report image
        template_path (str, optional): Path to the email template file
    
    Returns:
        tuple: (subject, body_html) for the email
    """
    logger.info(f"Preparing email for {contact_info.get('first_name', '')} at {contact_info.get('company_name', '')}")
    
    # Use default template if none provided
    if not template_path:
        template_path = 'default_email.html'
    
    # Load template
    template = env.get_template(template_path)
    
    # Set up template variables
    template_vars = {
        'first_name': contact_info.get('first_name', 'there'),
        'last_name': contact_info.get('last_name', ''),
        'company_name': contact_info.get('company_name', 'your company'),
        'website': contact_info.get('website', ''),
        'semrush_image_url': semrush_image_url,
        'sender_name': os.getenv('SENDER_NAME', 'Your Name'),
        'sender_title': os.getenv('SENDER_TITLE', 'Your Title'),
        'sender_company': os.getenv('SENDER_COMPANY', 'Your Company')
    }
    
    # Render the template
    body_html = template.render(**template_vars)
    
    # Create subject line
    subject = f"SEMRush Analysis for {template_vars['company_name']}"
    
    return subject, body_html 