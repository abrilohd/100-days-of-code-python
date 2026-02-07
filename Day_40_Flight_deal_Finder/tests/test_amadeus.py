import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://test.api.amadeus.com/v1/security/oauth2/token"

data = {
    "grant_type": "client_credentials",
    "client_id": os.getenv("AMADEUS_API_KEY"),
    "client_secret": os.getenv("AMADEUS_API_SECRET")
}

print("Testing connection to Amadeus...")
response = requests.post(url, data=data)
print(response.status_code)
print(response.text)
