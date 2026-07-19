# NetBox DEMO (GraphQL) – BEST Real Networking Example

This guide shows how to use the **NetBox DEMO GraphQL API** to retrieve real networking inventory data and save it to an **Excel** file using **Python + pandas**.

> NetBox DEMO is public/read‑only, so it’s safe for practice and video demos.

---

## What you’ll build
- Send a GraphQL query to NetBox DEMO
- Parse the JSON response
- Flatten the results into rows
- Save to **netbox_devices.xlsx** using pandas

---

## Step 1 — Open the NetBox DEMO GraphQL Playground
1. Open your browser.
2. Go to:

```
https://demo.netbox.dev/graphql/
```

You should see the GraphiQL interface (query editor on the left, results on the right).

---

## Step 2 — Install the requirements (one time)
Open a terminal/PowerShell in your working folder and run:

```bash
pip install requests pandas openpyxl
```

- **requests**: sends the HTTP POST to the GraphQL endpoint
- **pandas**: converts your data into a table
- **openpyxl**: lets pandas write `.xlsx`

---

## Step 3 — Create the Python script
Create a file named:

```
netbox_graphql_to_excel.py
```

Paste this **minimal** code:

```python
import requests
import pandas as pd
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://demo.netbox.dev/graphql/"

# Paste EXACTLY what NetBox shows (including the word Bearer)
token = "Bearer nbt_swa0Q5caACJR.kj3NC9Ylv8cPojiExQ82Yh6rt7XRpl0GxkuqLwM3"

query = """
{
  device_list {
    name
    site { name }
    primary_ip4 { address }
  }
}

"""

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": token,       
}

response = requests.post(url, json={"query": query}, headers=headers, timeout=30, verify=False)
print(response.status_code)

# Pretty print the full JSON response
print(json.dumps(response.json(), indent=4))


devices = response.json()["data"]["device_list"]


pd.json_normalize(devices).to_excel("netbox_devices.xlsx", index=False)
print("Saved netbox_devices.xlsx")
```

---

## Step 4 — Run the script
In the same folder where the script is saved:

```bash
python netbox_graphql_to_excel.py
```

After it runs, you should see:
- `netbox_devices.xlsx` created in the same folder
- A console message: `Saved netbox_devices.xlsx`

---

## Step 5 — (Optional) Quick troubleshooting
### If you get `ModuleNotFoundError: openpyxl`
Install it:

```bash
pip install openpyxl
```

### If the request fails (network/proxy)
Try:
- Confirm you can open `https://demo.netbox.dev/graphql/` in a browser
- Retry from another network
- If you’re behind a corporate proxy, configure proxy env vars or pass `proxies=` to `requests.post()`

---

## Step 6 — Video-friendly talking points (simple)
- “NetBox is a Network Source of Truth (inventory/IPAM/DCIM).”
- “GraphQL lets us request exactly the fields we want.”
- “We send one POST request, get JSON back, then export to Excel with pandas.”

---

## Next video ideas
- Export **interfaces** (second Excel sheet)
- Export **IP addresses** and filter by site
- Compare **NetBox REST vs GraphQL** (same output)

---

Happy automating 🚀
