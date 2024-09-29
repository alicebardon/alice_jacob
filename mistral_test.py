import requests
import os

# Set your Mistral API key as an environment variable
api_key = os.environ.get("MISTRAL_API_KEY")

# API endpoint
url = "https://api.mistral.ai/v1/chat/completions"

# Headers for the API request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Function to generate content using Mistral AI
def generate_content(prompt, model="mistral-tiny"):
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage
if __name__ == "__main__":
    prompt = "Write a one sentence story"
    result = generate_content(prompt)
    print(result)
