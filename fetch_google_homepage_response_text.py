import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

response = requests.get('https://google.com', verify=False)
if response.status_code == 200:
    print("Request successful")
else:
    print("Request failed with status code:", response.status_code)

print(response.text[:100])  # Print the first 100 characters of the response body


