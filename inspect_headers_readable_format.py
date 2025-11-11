import json
import requests

response = requests.get("https://api.github.com")

# Assuming you already have response.headers
headers = response.headers
print(type(headers))

print("\n--- JSON Format ---")
print(json.dumps(dict(headers), indent=4))

