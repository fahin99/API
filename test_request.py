import requests

for i in range(5):
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    if(response.status_code != 200):
        print("Failed to retrieve a joke")
        continue
    joke = response.json()
    print(f"{i+1}. Here's a random joke for you:\n")
    print(joke["setup"])
    print("👉", joke["punchline"])
