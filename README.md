# SalesAgent

## Overview
This project evaluates websites by pulling contact information from Apollo API, capturing website screenshots, and using OpenAI's GPT-4o model to classify websites based on their design and UX principles. The project generates both an HTML report and a CSV file containing websites that need improvement.

## Prerequisites
- Python 3.7 or higher
- Chrome browser installed (required for Selenium)
- API keys for:
  - Apollo (set via the `APOLLO_API_KEY` environment variable)
  - OpenAI (set via the `OPENAI_API_KEY` environment variable)

## Setup

1. **Clone the Repository** (if needed):
   ```bash
   git clone <repository_url>
   cd SalesAgent
   ```

2. **Create and Activate a Virtual Environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the project root with the following content:
   ```bash
   APOLLO_API_KEY=your_apollo_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```
   Replace `your_apollo_api_key` and `your_openai_api_key` with your actual API keys.

## Running the Project

To run the project, execute:

```bash
python classify_website.py
```

This script will:
1. Fetch contact information and website URLs from Apollo using a specific list ID
2. Process each website by:
   - Capturing a screenshot using Selenium
   - Analyzing the website design using OpenAI's GPT-4o model
   - Generating detailed UX/design feedback
3. Generate two outputs:
   - An HTML report (`report.html`) with screenshots and full classification results
   - A CSV file (`website_data.csv`) containing contact information for websites classified as "not good website"

## File Structure

- `requirements.txt`: Lists all Python dependencies
- `classify_website.py`: Main script that orchestrates the website classification process
- `apollo.py`: Handles fetching contact data from Apollo API
- `screenshot_capture.py`: Captures website screenshots using Selenium
- `report.html`: Generated report with screenshots and classification results
- `website_data.csv`: Generated CSV containing contact information for websites needing improvement

## Troubleshooting

- **Chrome and ChromeDriver**: Ensure Chrome is installed and compatible with the ChromeDriver version. The project uses `webdriver-manager` for automatic driver management.
- **API Keys**: Verify your API keys in the `.env` file if you encounter authentication issues.
- **Dependencies**: Ensure all dependencies are installed via `pip install -r requirements.txt`.
- **Apollo List ID**: The code is configured to pull contacts from a specific Apollo list (ID: 67a02758363e7e0021d20006). Update this ID in `apollo.py` if needed.

## Notes

- The project processes up to 60 websites per run
- Screenshots are saved as `screenshot_[number].png`
- The CSV file only includes websites classified as "not good website"
- For assistance or customization needs, please contact calvin@angusmadethis.com
