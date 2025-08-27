import requests

url="http://127.0.0.1:5000/"
data={
    "name": "John",
    "age": 30
}
response = requests.post(url, json=data)
print(response.json())