# --- Workout Tracking App ---
# Uses Nutritionix Natural Language API + Sheety API
# Secure version with Bearer Token authentication

import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Personal Data ---
GENDER = "male"
WEIGHT_KG = 70
HEIGHT_CM = 178
AGE = 22

# --- Nutritionix Credentials ---
APP_ID = os.environ["ENV_NIX_APP_ID"]
API_KEY = os.environ["ENV_NIX_API_KEY"]

# --- Nutritionix Endpoint ---
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

# --- Input from User ---
exercise_text = input(" Tell me which exercises you did: ")

# --- Nutritionix API Call ---
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

# --- Display Nutritionix Result ---
print("\n Nutritionix Data Received:")
for ex in result["exercises"]:
    print(f" - {ex['name'].title()}: {ex['duration_min']} min, {ex['nf_calories']} cal")

# --- Date & Time ---
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# --- Sheety Setup ---
GOOGLE_SHEET_NAME = "workout"   # must match your sheet tab name
sheet_endpoint = os.environ["ENV_SHEETY_ENDPOINT"]

# --- Sheety Authentication: Bearer Token ---
bearer_headers = {
    "Authorization": f"Bearer {os.environ['ENV_SHEETY_TOKEN']}"
}

# --- Loop through each exercise and add to Google Sheet ---
for exercise in result["exercises"]:
    sheet_inputs = {
        GOOGLE_SHEET_NAME: {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        headers=bearer_headers
    )

    print(f"Added to Google Sheet: {exercise['name'].title()} "
          f"({exercise['duration_min']} min, {exercise['nf_calories']} cal)")

print("\n All exercises have been logged successfully to your Google Sheet!")
