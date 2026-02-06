import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PIXELA_ENDPOINT = "https://pixe.la/v1/users"

USERNAME = os.getenv("PIXELA_USERNAME")
TOKEN = os.getenv("PIXELA_TOKEN")

GRAPH_ID = os.getenv("GRAPH_ID")
GRAPH_NAME = os.getenv("GRAPH_NAME")
GRAPH_UNIT = os.getenv("GRAPH_UNIT")
GRAPH_TYPE = os.getenv("GRAPH_TYPE")
GRAPH_COLOR = os.getenv("GRAPH_COLOR")

DATE_FORMAT = os.getenv("DATE_FORMAT", "%Y%m%d")

HEADERS = {
    "X-USER-TOKEN": TOKEN
}

# ----------------------
# Create User (run once)
# ----------------------
def create_user():
    payload = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }
    response = requests.post(PIXELA_ENDPOINT, json=payload)
    print(response.text)

# ----------------------
# Create Graph (run once)
# ----------------------
def create_graph():
    graph_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"
    graph_config = {
        "id": GRAPH_ID,
        "name": GRAPH_NAME,
        "unit": GRAPH_UNIT,
        "type": GRAPH_TYPE,
        "color": GRAPH_COLOR
    }
    response = requests.post(graph_endpoint, json=graph_config, headers=HEADERS)
    print(response.text)

# ----------------------
# Add Daily Pixel
# ----------------------
def add_pixel(quantity: str):
    today = datetime.now().strftime(DATE_FORMAT)
    endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}"
    pixel_data = {
        "date": today,
        "quantity": quantity
    }
    response = requests.post(endpoint, json=pixel_data, headers=HEADERS)
    print(response.text)

# ----------------------
# Update Pixel
# ----------------------
def update_pixel(quantity: str):
    today = datetime.now().strftime(DATE_FORMAT)
    endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}/{today}"
    response = requests.put(endpoint, json={"quantity": quantity}, headers=HEADERS)
    print(response.text)

# ----------------------
# Delete Pixel
# ----------------------
def delete_pixel():
    today = datetime.now().strftime(DATE_FORMAT)
    endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}/{today}"
    response = requests.delete(endpoint, headers=HEADERS)
    print(response.text)

# ----------------------
# Main Execution
# ----------------------
if __name__ == "__main__":
    amount = input("How many kilometres did you cycle today? ")
    add_pixel(amount)
