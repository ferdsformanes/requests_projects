import requests
import pandas as pd
import urllib3


# Disable SSL warnings (self-signed cert)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# DNAC Sandbox تفاصيل
BASE_URL = "https://sandboxdnac.cisco.com"
USERNAME = "devnetuser"
PASSWORD = "Cisco123!"

def get_token():
    url = f"{BASE_URL}/dna/system/api/v1/auth/token"
    response = requests.post(url, auth=(USERNAME, PASSWORD), verify=False)
    
    if response.status_code == 200:
        return response.json()["Token"]
    else:
        raise Exception(f"Auth failed: {response.text}")

def get_devices(token):
    url = f"{BASE_URL}/dna/intent/api/v1/network-device"
    headers = {
        "X-Auth-Token": token
    }

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        return response.json()["response"]
    else:
        raise Exception(f"Failed to fetch devices: {response.text}")
def main():
    token = get_token()
    devices = get_devices(token)

    df = pd.json_normalize(devices)

    # Keep only required columns and reorder them
    df = df[[
        "hostname",
        "managementIpAddress",
        "vendor",
        "platformId",
        "softwareVersion",
        "upTime",
        "serialNumber",
        "id",


    ]]

    df.to_excel("catalyst_center_devices.xlsx", index=False)


if __name__ == "__main__":
    main()

# API Ref: https://developer.cisco.com/docs/catalyst-center/authentication/#authentication
