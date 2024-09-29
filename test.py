from flask import Flask, jsonify, render_template_string
import os
import time
from lumaai import LumaAI
import requests
import json

# Import the Mistral API function
from mistral_test import generate_content

# Set the auth token from environment variable
auth_token = os.environ.get("LUMA_AUTH_TOKEN")
client = LumaAI(auth_token=auth_token)
app = Flask(__name__)

@app.route('/')  # Define a route for the root URL
def home():
    return "Welcome to the Flask app!"

@app.route('/generate', methods=['GET'])  # Define a route for video generation
def generate():
    url = "https://api.lumalabs.ai/dream-machine/v1/generations"
    headers = {
        'accept': 'application/json',
        'authorization': 'Bearer luma-4ddd7418-c15f-4bc9-ad91-14bf52bef1e8-5f250147-e74e-409c-9969-4ecd6c740087',  # Replace with your actual token
        'content-type': 'application/json',
    }

        # Generate prompt using Mistral AI
    ai_prompt = generate_content("Write a one sentence story")
    print(f"Generated prompt: {ai_prompt}")

    data = {
        "prompt": ai_prompt
    }

    # data = {
    #    "prompt": "In a quiet town, a lonely boy found a stray puppy, turning their shared loneliness into an unbreakable friendship."
    # }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    id = response.json()['id']


    print("Response:", response.json())


    while True:
        response = requests.get(f"{url}/{id}", headers=headers)
        response = response.json()
        print(response['state'])
        if response["state"] == 'completed':
            break
        time.sleep(2)

    # Access the video URL
    video_url = response['assets']['video']

    return render_template_string("""
    <!doctype html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Video Generation</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    padding: 20px;
                    max-width: 800px;
                    margin: 0 auto;
                }
                h1 {
                    color: #333;
                }
                .prompt {
                    background-color: #f4f4f4;
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Generated Video</h1>
                <div class="prompt">
                    <h2>Generated Prompt:</h2>
                <p>{{ prompt }}</p>
            </div>
            {% if video_url %}
                <video width="640" height="480" controls>
                    <source src="{{ video_url }}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            {% else %}
                <p>Video not generated. Please try again.</p>
            {% endif %}
        </body>
    </html>
    """, video_url=video_url, prompt=ai_prompt)

if __name__ == '__main__':
    app.run(debug=True)
