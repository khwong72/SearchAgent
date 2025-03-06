import os
import base64
import requests
import csv
import logging
import time
from datetime import datetime
from dotenv import load_dotenv
from screenshot_capture import capture_screenshot
from apollo import get_contacts_from_apollo

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.debug(f"Starting {func.__name__}")
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.debug(f"Finished {func.__name__} in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

# Log system info
logger.info("Python version: %s", os.sys.version)
logger.info("Starting program...")

start_time = time.time()
logger.info("Starting import of OpenAI...")
from openai import OpenAI  # New import style
logger.info("OpenAI import complete")

# Load environment variables
logger.info("Loading environment variables...")
load_dotenv()

# Initialize OpenAI client (new style)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY environment variable is not set.")
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
logger.info("API key loaded successfully")

client = OpenAI(api_key=api_key)  # New client initialization

@timer_decorator
def classify_website(website_url, screenshot_file="screenshot.png"):
    logger.info(f"Processing website: {website_url}")
    
    # Capture screenshot
    start_time = time.time()
    logger.info(f"Capturing screenshot of {website_url}")
    try:
        capture_screenshot(website_url, screenshot_file)
        logger.info(f"Screenshot capture took {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Screenshot capture failed for {website_url}: {str(e)}")
        return "not good website\n- Unable to capture screenshot"
    
    # Encode image
    start_time = time.time()
    if not os.path.exists(screenshot_file):
        error_msg = f"Screenshot file not found: {screenshot_file}"
        logger.error(error_msg)
        return f"not good website\n- {error_msg}"
        
    try:
        with open(screenshot_file, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        logger.info(f"Image encoding took {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Image encoding failed: {str(e)}")
        return "not good website\n- Failed to process screenshot"
    
    # Prepare messages for GPT‑4o
    messages = [
    {
        "role": "system",
        "content": (
            "You are GPT-4o, an expert in evaluating modern business websites for user-centric design, "
            "visual appeal, and effective UX. You will receive a screenshot of a website and analyze it "
            "using the following criteria from 'Modern Business Website Design: Principles for Engagement "
            "and UX':\n\n"
            "1. **Visual Design**: Color usage and branding, cohesive palette, typography clarity/hierarchy, "
            "   use of high-quality/optimized imagery, and sufficient whitespace.\n"
            "2. **Layout & Structure**: Clear hierarchy of content, grid systems or alignment, effective use "
            "   of whitespace, logical grouping of elements, and scannability.\n"
            "3. **Navigation & Accessibility**: Intuitive menus, consistent navigation patterns, adequate "
            "   color contrast, alt text on images, keyboard-friendly controls, and compliance with basic "
            "   accessibility practices.\n"
            "4. **Interactivity & Engagement**: Micro-interactions (hover states, button feedback), subtle "
            "   animations/transition effects, and purposeful interactive features that enrich the user "
            "   experience.\n"
            "5. **Modern Trends**: Thoughtful inclusion of trends like dark mode, glassmorphism, "
            "   neumorphism, AI personalization, or immersive/3D elements—only if they enhance usability.\n"
            "6. **Conversion Optimization**: Placement and clarity of CTAs, trust signals (testimonials, "
            "   security badges), streamlined form design, and overall persuasiveness.\n"
            "7. **Mobile Optimization**: Fully responsive layout, legible touch targets, well-structured "
            "   content on small screens, and minimal load times.\n"
            "8. **UX Enhancements & Performance**: Fast page loads, intuitive user feedback (loading states, "
            "   success/error messages), easily digestible content, and continuous improvement signals (e.g., "
            "   A/B tested elements).\n\n"
            "After examining the screenshot, you **must**:\n"
            "- Begin your response with exactly one of these phrases on its own line: 'good website' or "
            "  'not good website'.\n"
            "- Follow that verdict with bullet points summarizing how well (or poorly) the site meets the "
            "  above criteria.\n"
            "- If you judge the site as 'not good website', identify the highest-priority fixes. Keep the "
            "  focus on design, structure, UX, and performance aspects.\n\n"
            "Your goal is to provide a concise but thorough analysis that references specific design "
            "principles rather than just general impressions."
        )
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": (
                    "Here is a screenshot of a website. Please evaluate it according to the modern business "
                    "web design best practices in your instructions. Then give a final verdict ('good website' "
                    "or 'not good website') plus bullet points explaining why."
                )
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{encoded_image}"
                }
            }
        ]
    }
]


    
    # API call
    start_time = time.time()
    logger.info("Preparing API call...")
    try:
        response = client.chat.completions.create(  # Updated API call syntax
            model="gpt-4o",  # Updated model name
            messages=messages,
            max_tokens=1000,
            temperature=0.2,
        )
        logger.info(f"API call took {time.time() - start_time:.2f} seconds")
        
        classification_result = response.choices[0].message.content
        if not classification_result:
            logger.error("Empty response from API")
            return "not good website\n- Analysis failed due to empty API response"
            
        logger.info("Classification result received")
        return classification_result
        
    except Exception as e:
        error_msg = f"Error in API call: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return f"not good website\n- Analysis failed: {error_msg}"

def generate_html_report(results, output_file):
    logger.info(f"Generating HTML report to {output_file}")
    html = [
        "<html>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<title>Website Classification Report</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; }",
        "img { max-width: 600px; border: 1px solid #ccc; margin: 10px 0; }",
        "h2 { color: #333; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Website Classification Report</h1>",
    ]
    
    for website, (screenshot_file, classification) in results.items():
        logger.debug(f"Adding report entry for {website}")
        html.append(f"<h2>{website}</h2>")
        if os.path.exists(screenshot_file):
            # Read and encode the screenshot
            with open(screenshot_file, "rb") as img_file:
                encoded_img = base64.b64encode(img_file.read()).decode("utf-8")
            html.append(f'<img src="data:image/png;base64,{encoded_img}" alt="Screenshot of {website}"/>')
        else:
            logger.warning(f"Screenshot not found for {website}")
            html.append("<p>[Screenshot not found]</p>")
        html.append(f"<p><strong>Classification:</strong> {classification}</p>")
        html.append("<hr/>")
    
    html.append("</body></html>")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    logger.info(f"HTML report generated: {output_file}")

def get_simplified_company_name(company_name):
    if not company_name:
        return ""
        
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at simplifying company names to how they would be referred to in casual conversation. Remove suffixes like Inc, LLC, Corp etc. Return only the simplified name in title case."
                },
                {
                    "role": "user",
                    "content": f"Simplify this company name: {company_name}"
                }
            ],
            max_tokens=50,
            temperature=0
        )
        simplified_name = response.choices[0].message.content.strip()
        return simplified_name
    except Exception as e:
        logger.error(f"Error simplifying company name: {str(e)}")
        return company_name.title()

def write_csv_report(not_good_rows, csv_file):
    logger.info(f"Writing CSV report to {csv_file}")
    fieldnames = ["website", "company_name", "first_name", "last_name", "email", "location"]
    try:
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in not_good_rows:
                # Get simplified company name
                simplified_name = get_simplified_company_name(row.get("company_name", ""))
                row["company_name"] = simplified_name
                writer.writerow(row)
        logger.info(f"CSV report generated: {csv_file}")
    except Exception as e:
        logger.error(f"Error writing CSV report: {str(e)}", exc_info=True)

@timer_decorator
def main():
    # Get number of websites from command line argument
    import sys
    if len(sys.argv) != 2:
        logger.error("Usage: python3 classify_website.py <number_of_websites>")
        sys.exit(1)
    try:
        num_websites = int(sys.argv[1])
    except ValueError:
        logger.error("Please provide a valid number")
        sys.exit(1)

    logger.info("Starting main process")
    
    start_time = time.time()
    contacts = get_contacts_from_apollo()
    logger.info(f"Apollo API call took {time.time() - start_time:.2f} seconds")
    logger.info(f"Retrieved {len(contacts)} contacts")
    
    # Get the list name from apollo.py
    from apollo import CURRENT_LIST_NAME
    
    # Create screenshots directory if it doesn't exist
    screenshots_dir = CURRENT_LIST_NAME
    os.makedirs(screenshots_dir, exist_ok=True)
    logger.info(f"Saving screenshots to directory: {screenshots_dir}")
    
    results = {}
    not_good_rows = []
    
    for i, contact in enumerate(contacts[:num_websites], start=1):
        website = contact["website"]
        screenshot_file = f"{screenshots_dir}/screenshot_{i}.png"
        logger.info(f"Processing website {i}/{num_websites}: {website}")
        
        classification = classify_website(website, screenshot_file=screenshot_file)
        results[website] = (screenshot_file, classification)
        
        if classification and "not good" in classification.lower():
            not_good_rows.append({
                "website": website,
                "company_name": contact.get("company_name", ""),
                "first_name": contact.get("first_name", ""),
                "last_name": contact.get("last_name", ""),
                "email": contact.get("email", ""),
                "location": contact.get("location", "")
            })
    
    logger.info("Generating reports...")
    
    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%H-%M-%S_%m-%d-%Y")
    csv_file = f"ng_{timestamp}.csv"
    html_file = f"ng_{timestamp}.html"
    
    if not_good_rows:
        write_csv_report(not_good_rows, csv_file)
    generate_html_report(results, html_file)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error("Fatal error in main", exc_info=True)
        raise
