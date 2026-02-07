import os
import requests
from datetime import datetime
from flight_data import FlightData
from dotenv import load_dotenv

load_dotenv()

AMADEUS_ENV = "test"  # "test" or "production"
BASE_URL = "https://test.api.amadeus.com" if AMADEUS_ENV == "test" else "https://api.amadeus.com"


class FlightSearch:
    def __init__(self):
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = f"{BASE_URL}/v1/security/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        token = response.json()["access_token"]
        return token

    def get_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        url = f"{BASE_URL}/v2/shopping/flight-offers"
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "max": 1,
            "currencyCode": "GBP"
        }
        response = requests.get(url, headers=self.get_headers(), params=query)
        data = response.json()

        if "errors" in data:
            print(f"No flights found for {destination_city_code}: {data['errors']}")
            return None

        offer = data["data"][0]
        flight_data = FlightData(
            price=offer["price"]["total"],
            origin_city=offer["itineraries"][0]["segments"][0]["departure"]["iataCode"],
            origin_airport=offer["itineraries"][0]["segments"][0]["departure"]["iataCode"],
            destination_city=offer["itineraries"][0]["segments"][-1]["arrival"]["iataCode"],
            destination_airport=offer["itineraries"][0]["segments"][-1]["arrival"]["iataCode"],
            out_date=offer["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0],
            return_date=offer["itineraries"][0]["segments"][-1]["arrival"]["at"].split("T")[0],
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data
