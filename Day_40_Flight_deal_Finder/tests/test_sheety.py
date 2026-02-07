import requests

url = "https://api.sheety.co/9f5c37993ce02af09e8d5fa96b47c71c/flightsearch/prices"

try:
    response = requests.get(url)
    response.raise_for_status()
    print(response.json())
except Exception as e:
    print("Error:", e)
