# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

# Sheety
SHEETY_PRICES_ENDPOINT = os.getenv("SHEETY_PRICES_ENDPOINT")

# Twilio
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = os.getenv("TWILIO_VIRTUAL_NUMBER")
TWILIO_VERIFIED_NUMBER = os.getenv("TWILIO_VERIFIED_NUMBER")

# Amadeus - support both older and newer env var names for compatibility
AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY") or os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET") or os.getenv("AMADEUS_CLIENT_SECRET")
AMADEUS_USE_PRODUCTION = os.getenv("AMADEUS_USE_PRODUCTION", "false").lower() in ("1", "true", "yes")

# Email
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
