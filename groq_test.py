import requests
import base64
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env file

# Load and encode the image as base64 (Groq expects base64 image strings)
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Replace with your Groq API key
API_KEY = os.getenv("GROQ_API_KEY")

# Groq endpoint and model
url = "https://api.groq.com/openai/v1/chat/completions"
model = "llama-3.2-90b-vision-preview"

# Base64-encoded image
image_path = "example.png"
image_b64 = encode_image(image_path)

# Construct payload with image and text
payload = {
    "model": model,
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What’s happening in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_b64}"
                    }
                }
            ]
        }
    ],
    "temperature": 0.2
}

# Send request to Groq
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
response = requests.post(url, json=payload, headers=headers)

# Print response from Groq
print(response.json())
