import json

with open("data.json", "r") as file:
    data = json.load(file)
print(data)

with open("data2.json", "w") as file:
    json.dump(data, file, indent = 4)


# data = json.loads(json_string)
# data[0]["name"] = "Tim"
# data = json.dumps(data, indent=4)

