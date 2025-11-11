import requests
import urllib3

# Disable SSL warnings (because verify=False is used)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URLS = ["https://api.github.com", "https://api.github.com/invalid"]

for url in URLS:
    print(f"Checking URL: {url}")
    try:
        # Send GET request (skip SSL check, 10s timeout)
        response = requests.get(url, verify=False, timeout=10)
        # Raise error for bad status codes
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Handle any request-related error (network error, timeout, HTTP error, etc.)
        print(f"Error for {url}: {e}")
    else:
        # Runs only if no error occurred
        print(f"Success! Status Code: {response.status_code}")
