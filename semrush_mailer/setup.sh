#!/bin/bash
# Setup script for SEMRush Mailer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements with explicit versions
pip install selenium==4.15.2
pip install webdriver-manager==4.0.1
pip install requests==2.31.0
pip install python-dotenv==1.0.0
pip install jinja2==3.1.2

# Create templates directory
mkdir -p templates
mkdir -p semrush_reports
mkdir -p email_previews

echo "Setup complete! Run 'python3 csv_test.py sample_contacts.csv 1' to start." 