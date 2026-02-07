import os
import requests
import time
import random
from datetime import timedelta
from dotenv import load_dotenv

from flight_data import FlightData

load_dotenv()


class FlightSearch:
    """Provides either real Amadeus lookups (when credentials exist)
    or a safe mocked fallback so the project can run without network credentials.
    """

    TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"

    def __init__(self):
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self.access_token = None

    def get_access_token(self):
        """Attempt to retrieve an access token from Amadeus (3 retries).
        If credentials are not provided, returns None and leaves client in mock mode.
        """
        if not (self.api_key and self.api_secret):
            print("[FlightSearch] No Amadeus credentials found; running in mock mode.")
            return None

        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }

        last_exception = None
        for attempt in range(3):
            try:
                print(f"[FlightSearch] Token attempt {attempt+1}/3...")
                resp = requests.post(self.TOKEN_URL, data=data, timeout=20)
                resp.raise_for_status()
                token = resp.json().get("access_token")
                self.access_token = token
                print("[FlightSearch] Token received successfully.")
                return token
            except Exception as e:
                print(f"[FlightSearch] Token attempt {attempt+1}/3 failed: {e}")
                last_exception = e
                time.sleep(2)

        raise RuntimeError("Failed to get Amadeus access token") from last_exception

    def get_destination_code(self, city_name: str) -> str:
        """Return IATA code for a city name.
        If Amadeus credentials are available, an API call would be made.
        Otherwise, return a simple fallback: first 3 uppercase letters.
        """
        if self.api_key and self.api_secret:
            try:
                # Attempt a simple locations lookup using the Amadeus test endpoint
                token = self.access_token or self.get_access_token()
                headers = {"Authorization": f"Bearer {token}"}
                params = {"keyword": city_name, "subType": "CITY"}
                url = "https://test.api.amadeus.com/v1/reference-data/locations"
                resp = requests.get(url, headers=headers, params=params, timeout=15)
                resp.raise_for_status()
                data = resp.json()
                locations = data.get("data") or []
                if locations:
                    return locations[0].get("iataCode") or city_name[:3].upper()
            except Exception as e:
                print(f"[FlightSearch] Location lookup failed for {city_name}: {e}")

        # Fallback: use first 3 letters of the city name as a naive IATA
        return city_name.replace(" ", "")[:3].upper()

    def check_flights(self, origin_iata: str, destination_iata: str, from_time, to_time):
        """Return a FlightData object or None.
        This implementation provides a mocked flight when no Amadeus credentials
        are configured so the rest of the project can run offline.
        """
        # If Amadeus credentials are missing, return a mocked flight
        if not (self.api_key and self.api_secret):
            # produce a mock price between 50 and 800
            price = float(random.randint(50, 800))
            out_date = from_time.date().isoformat() if hasattr(from_time, "date") else str(from_time)
            return_date = (from_time + timedelta(days=7)).date().isoformat() if hasattr(from_time, "date") else str(to_time)
            return FlightData(
                price=price,
                origin_city=origin_iata,
                origin_airport=f"{origin_iata} Airport",
                destination_city=destination_iata,
                destination_airport=f"{destination_iata} Airport",
                out_date=out_date,
                return_date=return_date,
            )

        # Real implementation placeholder: attempt a simple offers lookup.
        try:
            token = self.access_token or self.get_access_token()
            headers = {"Authorization": f"Bearer {token}"}
            # Amadeus new Flight Offers endpoint requires specific query params
            params = {
                "originLocationCode": origin_iata,
                "destinationLocationCode": destination_iata,
                "departureDate": from_time.date().isoformat(),
                "adults": 1,
                "max": 1,
            }
            url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
            resp = requests.get(url, headers=headers, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            offers = data.get("data") or []
            if not offers:
                return None

            offer = offers[0]
            # Amadeus response parsing is simplified here; real code should be more defensive
            price = float(offer.get("price", {}).get("grandTotal", 0) or 0)
            out_date = offer.get("itineraries", [])[0].get("segments", [])[0].get("departure", {}).get("at")
            return_date = offer.get("itineraries", [])[0].get("segments", [])[0].get("arrival", {}).get("at")
            origin_city = origin_iata
            dest_city = destination_iata
            return FlightData(
                price=price,
                origin_city=origin_city,
                origin_airport=f"{origin_iata} Airport",
                destination_city=dest_city,
                destination_airport=f"{destination_iata} Airport",
                out_date=out_date,
                return_date=return_date,
            )
        except Exception as e:
            print(f"[FlightSearch] Error checking flights: {e}")
            return None
