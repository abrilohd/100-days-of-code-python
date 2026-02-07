# data_manager.py
import requests
from config.settings import SHEETY_PRICES_ENDPOINT

class DataManager:
    def __init__(self):
        self.destination_data = []

    def get_destination_data(self):
        if not SHEETY_PRICES_ENDPOINT:
            raise ValueError("SHEETY_PRICES_ENDPOINT is not set in environment.")
        resp = requests.get(SHEETY_PRICES_ENDPOINT, timeout=20)
        resp.raise_for_status()
        self.destination_data = resp.json().get("prices", [])
        return self.destination_data

    def update_destination_codes(self):
        if not self.destination_data:
            return
        for city in self.destination_data:
            if not city.get("iataCode"):
                continue
            new_data = {"price": {"iataCode": city["iataCode"]}}
            resp = requests.put(f"{SHEETY_PRICES_ENDPOINT}/{city['id']}", json=new_data, timeout=20)
            if resp.ok:
                print(f"Updated {city['city']} -> {city['iataCode']}")
            else:
                print(f"Failed to update {city['city']}: {resp.status_code} {resp.text}")
