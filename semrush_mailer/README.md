# SEMRush Mailer

Automated tool for generating and sending SEMRush reports via email.

## Overview

This tool automates the process of:
1. Capturing SEMRush reports for specified websites
2. Generating personalized emails with embedded reports
3. Sending emails through Mailgun (or alternatively, Gmail)

## Setup

1. Install dependencies:
```bash
./setup.sh
# or
pip3 install -r requirements.txt
```

2. Configure environment variables:
Copy `.env.example` to `.env` and fill in:
```
# SEMRush credentials
SEMRUSH_EMAIL=your_email
SEMRUSH_PASSWORD=your_password

# Email sender information
SENDER_NAME=Your Name
SENDER_TITLE=Your Title
SENDER_COMPANY=Your Company

# Mailgun credentials
MAILGUN_API_KEY=your_mailgun_key
MAILGUN_DOMAIN=your_domain
```

## Usage

1. Prepare a CSV file with contacts:
```csv
email,first_name,last_name,company_name,website
example@company.com,John,Doe,Company Inc,company.com
```

2. Run the script:
```bash
python3 csv_test.py your_contacts.csv [number_of_contacts]
```

Example:
```bash
python3 csv_test.py test_contact.csv 1  # Process one contact
```

## Components

- `csv_test.py`: Main script orchestrating the process
- `semrush_capture.py`: Handles SEMRush login and report capture
- `mailgun_sender.py`: Manages email sending through Mailgun
- `email_preparer.py`: Prepares email templates and content
- `gmail_sender.py`: Alternative email sender using Gmail
- `apollo_sender.py`: Legacy Apollo integration

## Output

- Generated reports: `semrush_reports/`
- Email previews: `email_previews/`
- Debug screenshots: Saved during SEMRush capture process

## Troubleshooting

- Check Chrome/ChromeDriver compatibility
- Verify SEMRush credentials
- Ensure Mailgun API key has proper permissions
- Look for debug screenshots if SEMRush capture fails

## Notes

- Uses Selenium in visible mode for debugging
- Supports base64-encoded images in emails
- Includes error handling and logging
- Can process multiple contacts in batch 