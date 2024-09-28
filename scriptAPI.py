import os
from lumaai import LumaAI

auth_token = os.environ.get("LUMA_AUTH_TOKEN")
client = LumaAI(auth_token=auth_token)

try:
    # Test making a simple request to the API
    response = client.generations.create(prompt="Test prompt")
    print(response)
except Exception as e:
    print("API Connection Error:", e)

auth_token = os.environ.get("LUMA_AUTH_TOKEN")
print("Auth Token:", auth_token)
