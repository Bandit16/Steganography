import requests

endpoint = "http://127.0.0.1:8000/api/encode/"

data = {
    "Message": "checking api"
}

files = {
    "File": open("/Users/dipeshacharya/Desktop/nagarikta1.jpg", "rb"),
    "Image": open("/Users/dipeshacharya/Desktop/hackathon/minor_project/test.png", "rb")
}

response = requests.post(endpoint, data=data, files=files)
print(response.json())