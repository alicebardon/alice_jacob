import requests
import json
import time

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



print(response['assets']['video'])
