import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

response = requests.get("https://api.thecatapi.com/v1/breeds", verify=False)

if response.status_code == 200:
    print("Request successful")
    data = response.json()
    print(json.dumps(data, indent=2)[:1000])  # Print the first 500 characters of the formatted JSON response
else:
    print("Request failed with status code:", response.status_code) 