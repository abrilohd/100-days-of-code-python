import requests
from datetime import datetime

pixela_endpoint = "https://pixe.la/v1/users"
USERNAME = "abrsh"
TOKEN = "hjkp12pnm12nmjk27"
GRAPH = "graph1"

user_params = {
    "token": USERNAME,
    "username": TOKEN,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config= {
    "id": GRAPH,
    "name": "Cycling Graph",
    "unit":"km",
    "type":"float",
    "color": "ajisai"
}

headers = {
    "X-USER-TOKEN": TOKEN
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers= headers)
# print(response.text)

pixel_creation_endpoint = "/v1/users/<username>/graphs/<graphID>"

today = datetime.now()
# print(today.strftime("%Y%m%d"))

pixel_data = {
    "date": today.strftime("%Y%m%d"),
    "quantity": input("how many kilometres did you cycle today? "),
}

post = f"{graph_endpoint}/{GRAPH}"
response = requests.post(url=post, json=pixel_data, headers=headers)
print(response.text)

update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH}/{today.strftime('%Y%m%d')}"

update_config = {
    "quantity": "4.0",
}

# response = requests.put(url=update_endpoint, json=update_config, headers=headers)
# print(response.text)

delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH}/{today.strftime('%Y%m%d')}"

# response = requests.delete(url=delete_endpoint, headers=headers)
# print(response.text)