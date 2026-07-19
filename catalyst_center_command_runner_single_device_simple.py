import json
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://sandboxdnac.cisco.com"
USERNAME = "devnetuser"
PASSWORD = "Cisco123!"

AUTH_URL = "/dna/system/api/v1/auth/token"
DEVICES_URL = "/dna/intent/api/v1/network-device"
COMMAND_URL = "/dna/intent/api/v1/network-device-poller/cli/read-request"
TASK_URL = "/dna/intent/api/v1/task/{}"
FILE_URL = "/dna/intent/api/v1/file/{}"


# 1. Get token
def get_token():
    r = requests.post(
        BASE_URL + AUTH_URL,
        auth=(USERNAME, PASSWORD),
        verify=False
    )
    return r.json()["Token"]


# 2. Get first device
def get_device(headers):
    r = requests.get(BASE_URL + DEVICES_URL, headers=headers, verify=False)
    device = r.json()["response"][0]
    return device["id"], device["hostname"]


# 3. Send command
def run_command(headers, device_id):
    payload = {
        "commands": ["show ip int brief"],
        "deviceUuids": [device_id],
        "timeout": 0
    }

    r = requests.post(BASE_URL + COMMAND_URL, json=payload, headers=headers, verify=False)
    return r.json()["response"]["taskId"]


# 4. Wait for file ID
def get_file_id(headers, task_id):
    while True:
        r = requests.get(
            BASE_URL + TASK_URL.format(task_id),
            headers=headers,
            verify=False
        )
        progress = r.json()["response"]["progress"]
        if "fileId" in progress:
            progress_data = json.loads(progress)
            return progress_data["fileId"]

        print("Waiting...")
        time.sleep(2)

# 5. Get output
def get_output(headers, file_id):
    r = requests.get(BASE_URL + FILE_URL.format(file_id), headers=headers, verify=False)
    return r.json()


def main():

    token = get_token()
    headers = {"X-Auth-Token": token}

    device_id, hostname = get_device(headers)

    print("Device:", hostname)

    task_id = run_command(headers, device_id)
    print("Task ID:", task_id)

    file_id = get_file_id(headers, task_id)
    print("File ID:", file_id)

    result = get_output(headers, file_id)

    output = result[0]["commandResponses"]["SUCCESS"]["show ip int brief"]

    print("\n==============================")
    print("DEVICE:", hostname)
    print("==============================\n")
    print(output)


if __name__ == "__main__":
    main()

# References: https://developer.cisco.com/docs/catalyst-center/command-runner/#endpoints-and-methods-used
