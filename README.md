# SearchAgent

A comprehensive sales automation toolkit that combines website analysis, SEMRush reporting, and automated email outreach.

## Project Components

### 1. SEMRush Mailer (`/semrush_mailer`)
Automates the process of generating and sending SEMRush reports via email.
- `csv_test.py`: Main script for processing contacts and sending reports
- `semrush_capture.py`: Captures SEMRush reports using Selenium
- `mailgun_sender.py`: Handles email delivery through Mailgun
- `email_preparer.py`: Prepares email templates and content
- `apollo_sender.py`: (Legacy) Apollo API integration
- `gmail_sender.py`: (Alternative) Gmail integration

### 2. Website Analysis (`/`)
Tools for analyzing and classifying websites:
- `classify_website.py`: Main classification script using GPT-4
- `screenshot_capture.py`: Captures website screenshots
- `apollo.py`: Apollo API integration for contact data

### 3. Utilities
- `list_models.py`: OpenAI model management
- `testing.py`: Test scripts
- `upload.py`: File upload utilities

## Setup

1. Clone the repository:
```bash
git clone https://github.com/calvinbeighle/SearchAgent.git
cd SearchAgent
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file with:
```
# SEMRush credentials
SEMRUSH_EMAIL=your_email
SEMRUSH_PASSWORD=your_password

# Email sender information
SENDER_NAME=Your Name
SENDER_TITLE=Your Title
SENDER_COMPANY=Your Company

# Mailgun credentials (for email sending)
MAILGUN_API_KEY=your_mailgun_key
MAILGUN_DOMAIN=your_domain

# Optional API keys
APOLLO_API_KEY=your_apollo_key
OPENAI_API_KEY=your_openai_key
```

## Usage

### SEMRush Report Generation and Emailing
```bash
cd semrush_mailer
python3 csv_test.py test_contact.csv 1
```
This will:
1. Read contacts from CSV
2. Capture SEMRush reports
3. Generate email previews
4. Send emails through Mailgun

### Website Classification
```bash
python3 classify_website.py
```
This will:
1. Analyze websites using GPT-4
2. Generate screenshots
3. Create classification reports

## Project Structure
```
SearchAgent/
├── semrush_mailer/           # SEMRush report automation
│   ├── templates/            # Email templates
│   ├── email_previews/      # Generated email previews
│   └── semrush_reports/     # Captured SEMRush reports
├── csvs/                    # CSV data files
├── oldreports/             # Historical reports
├── oldscreenshots/         # Historical screenshots
└── test/                   # Test files
```

## Features

- **Automated SEMRush Reports**: Captures and processes SEMRush data
- **Email Integration**: Supports multiple email providers (Mailgun, Gmail)
- **Contact Management**: Integration with Apollo for contact data
- **Website Analysis**: AI-powered website classification
- **Customizable Templates**: Email template system
- **Batch Processing**: Handle multiple contacts efficiently

## Dependencies

- Python 3.7+
- Selenium WebDriver
- Chrome/Chromium browser
- Required Python packages in `requirements.txt`

## Notes

- Generated reports are saved in `semrush_reports/`
- Email previews are stored in `email_previews/`
- Supports batch processing of contacts
- Includes error handling and logging

## Contributing

Feel free to submit issues and enhancement requests.

## Contact

Calvin Beighle - calvin@angusdesign.com
