import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

API_KEY = os.getenv("OWM_API_KEY")
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
TO_NUMBER = os.getenv("TWILIO_TO_NUMBER")

LAT = os.getenv("LATITUDE")
LON = os.getenv("LONGITUDE")

weather_params = {
    "lat": LAT,
    "lon": LON,
    "appid": API_KEY,
    "cnt": 4,
}

response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False

for hour in weather_data["list"]:
    condition_code = hour["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True
        break

if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body="🌧️ Rain Alert: It's going to rain today. Bring an umbrella!",
        from_=FROM_NUMBER,
        to=TO_NUMBER
    )
    print("SMS sent:", message.sid)
else:
    print("No rain expected 🌤️")
