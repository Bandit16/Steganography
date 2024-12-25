import requests

endpoint = "http://127.0.0.1:8000/"

with open("new_test.png", "rb") as image_file:
    files = {"Image": image_file}
    data = {"Message": "I am dipesh"}
    response = requests.post(endpoint, files=files, data=data)
    print(response.json())