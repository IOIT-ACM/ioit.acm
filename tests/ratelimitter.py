import requests


# config.py
class Config:
    BASE_URL = "http://127.0.0.1:5001"
    MAX_REQUESTS = 500
    ENDPOINTS = ["/", "/events", "/profile", "/about", "/competitions"]
    METHODS = ["GET", "POST"]
    PAYLOAD = {"username": "user", "password": "admin"}


method = Config.METHODS[0]
attempts = Config.MAX_REQUESTS
endpoint = Config.ENDPOINTS[0]

url = Config.BASE_URL + endpoint
print(f"Testing {method} request to {url}")

try:
    for attempt in range(1, attempts + 1):
        if method == "POST":
            response = requests.post(url, data=Config.PAYLOAD)
        else:
            response = requests.get(url)

        print(f"Attempt {attempt}: Status Code {response.status_code}")

        if response.status_code == 429:
            print("Rate limit exceeded!")
            break

except requests.RequestException as e:
    print(f"An error occurred: {e}")
