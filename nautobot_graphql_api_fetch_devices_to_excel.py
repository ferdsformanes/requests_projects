import requests
import pandas as pd
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://demo.nautobot.com/api/graphql/"  # API endpoint 

headers = {
    "Authorization": "Token aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

query = """
{
  devices {
    name
    status { name }
    location { name }
    primary_ip4 { address }
  }
}
"""


resp = requests.post(url, json={"query": query}, headers=headers, verify=False, timeout=30)
payload = resp.json()["data"]["devices"]  # should be the list of devices

print(type(payload))  # should be a list of dictionaries

df = pd.json_normalize(payload)

# Remove the nested-object column; keep only the flattened address column
df = df.drop(columns=["primary_ip4"], errors="ignore")

df.to_excel("nautobot_devices.xlsx", index=False, engine="openpyxl")