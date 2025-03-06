# SEMRush Mailer

This program captures screenshots of SEMRush reports for websites and sends them via Apollo's mail merge functionality.

## Setup

1. Run the setup script:
   ```
   chmod +x setup.sh
   ./setup.sh
   ```

2. Add your API keys to a `.env` file:
   ```
   APOLLO_API_KEY=your_apollo_api_key
   OPENAI_API_KEY=your_openai_api_key
   SENDER_NAME=Your Name
   SENDER_TITLE=Your Position
   SENDER_COMPANY=Your Company
   ```

## Usage

Run the main script with the number of contacts to process:

```
python3 main.py 10
```

This will:
1. Fetch contacts from Apollo
2. Capture SEMRush reports for each website
3. Upload the reports to Apollo
4. Create an email template with the reports embedded
5. Start an email sequence to send the emails

## Customization

You can customize the email template by editing the file in the `templates` directory. The default template includes:
- Personalized greeting
- SEMRush report image
- Call-to-action button
- Your signature

## Troubleshooting

If you encounter issues:
- Check that your API keys are correct
- Ensure you have proper permissions in Apollo
- Check the logs for detailed error messages 