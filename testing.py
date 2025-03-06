import base64
import os
import openai

############################################################################
# 1. Set API key and base URL correctly
############################################################################
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ensure the correct base URL (without extra /chat/completions)
openai.api_base = os.getenv("GPT4O_API_BASE", "https://api.openai.com/v1")

############################################################################
# 2. Encode the screenshot properly
############################################################################
image_file_path = "test_screenshot.png"
if not os.path.exists(image_file_path):
    raise FileNotFoundError(f"Screenshot not found: {image_file_path}")

with open(image_file_path, "rb") as f:
    encoded_image = base64.b64encode(f.read()).decode("utf-8")

############################################################################
# 3. Construct messages using correct OpenAI format
############################################################################
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": (
                    "Here is an image. Please describe exactly what you see in it. "
                    "What color is the largest section and any major text visible?"
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

############################################################################
# 4. Make the ChatCompletion call using the correct format
############################################################################
try:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=300
    )
    print(response.choices[0].message.content)

except Exception as e:
    print("Error from GPT-4o endpoint:", e)
