import os
import requests

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"  # Update with actual API URL
API_KEY = os.getenv("5V66nCpJWSWwsldfu2zYRKBjujiMw2CO")  # Store your API key in environment variables

def query_mistral_api(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "max_tokens": 500,  # Adjust based on the prompt size or API limits
    }

    response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)
    return response.json()

# Example usage
#prompt = "Extract key points from the following text: \n" + text  # `text` is the output from the PowerPoint extraction
#result = query_mistral_api(prompt)
#print(result)
