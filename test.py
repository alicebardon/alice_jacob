from flask import Flask, jsonify, render_template_string
import os
import time
from lumaai import LumaAI

# Set the auth token from environment variable
auth_token = os.environ.get("LUMA_AUTH_TOKEN")
client = LumaAI(auth_token=auth_token)
app = Flask(__name__)

@app.route('/')  # Define a route for the root URL
def home():
    return "Welcome to the Flask app!"

@app.route('/generate', methods=['GET'])  # Define a route for video generation
def generate():
    generation = client.generations.create(
        prompt="A teddy bear in sunglasses playing electric guitar and dancing",
    )
    
    video_id = generation.id  # Get the generation ID
    print(video_id)

    # Polling for the video generation to complete
    while True:
        video_generation = client.generations.get(id=video_id)
        
        # Check if the assets are available
        if video_generation.assets is not None:
            break
        
        # Optionally: Implement a timeout to prevent infinite loops
        time.sleep(2)  # Wait for a couple of seconds before checking again

    # Access the video URL
    video_url = video_generation.assets.video if video_generation.assets.video else None

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

print("Auth Token:", auth_token)
print(video_id)
