import requests
import urllib3
import json

# Disable SSL warnings (because verify=False is used)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://api.github.com"

response = requests.get(url, verify=False, timeout=10)

if response.status_code == 200:
    print("Request successful")
    bytes = response.content
    print(type(bytes))
    text = response.text
    print(type(text))
    data = response.json()
    print(type(data))
else:
    print("Request failed with status code:", response.status_code)
