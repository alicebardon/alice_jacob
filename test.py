from flask import Flask, jsonify, render_template_string
import os
import time
from lumaai import LumaAI
import requests
import json

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
    data = {
        "prompt": "an old lady laughing underwater, wearing a scuba diving suit"
    }

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
        </head>
        <body>
            <h1>Generated Video</h1>
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
    """, video_url=video_url)

if __name__ == '__main__':
    app.run(debug=True)
