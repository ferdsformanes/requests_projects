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
    r.raise_for_status()
    return r.json()["Token"]


# 2. Get all devices
def get_devices(headers):
    r = requests.get(BASE_URL + DEVICES_URL, headers=headers, verify=False)
    r.raise_for_status()

    devices = r.json()["response"]

    # Build a simple list with device ID and hostname
    device_list = []
    for device in devices:
        device_list.append({
            "id": device["id"],
            "hostname": device["hostname"]
        })

    return device_list


# 3. Send command to all devices
def run_command(headers, device_ids):
    # Send one CLI command to all device UUIDs
    payload = {
        "commands": ["show ip int brief"],
        "deviceUuids": device_ids,
        "timeout": 0
    }

    r = requests.post(
        BASE_URL + COMMAND_URL,
        json=payload,
        headers=headers,
        verify=False
    )
    r.raise_for_status()
    return r.json()["response"]["taskId"]


# 4. Wait for file ID
def get_file_id(headers, task_id):
    while True:
        r = requests.get(
            BASE_URL + TASK_URL.format(task_id),
            headers=headers,
            verify=False
        )
        r.raise_for_status()

        progress = r.json()["response"]["progress"]

        if progress:
            try:
                # Convert progress text into JSON
                progress_data = json.loads(progress)
                if "fileId" in progress_data:
                    return progress_data["fileId"]
            except json.JSONDecodeError:
                # Ignore if progress is not JSON yet
                pass

        print("Waiting...")
        time.sleep(2)


# 5. Get output
def get_output(headers, file_id):
    r = requests.get(
        BASE_URL + FILE_URL.format(file_id),
        headers=headers,
        verify=False
    )
    r.raise_for_status()
    return r.json()


def main():
    # Step 1: Authenticate and get an access token
    token = get_token()
    headers = {"X-Auth-Token": token}

    # Step 2: Retrieve all network devices
    devices = get_devices(headers)

    if not devices:
        print("No devices found.")
        return

    # Step 3: Extract all device UUIDs
    device_ids = [device["id"] for device in devices]

    print("Devices found:")
    for device in devices:
        print("-", device["hostname"])

    # Step 4: Send the CLI command to all devices
    task_id = run_command(headers, device_ids)
    print("\nTask ID:", task_id)

    # Step 5: Wait for the task to finish and retrieve the file ID
    file_id = get_file_id(headers, task_id)
    print("File ID:", file_id)

    # Step 6: Download the command outputs
    results = get_output(headers, file_id)

    print("\n==============================")
    print("COMMAND OUTPUTS")
    print("==============================\n")

    # Step 7: Display the output for each device
    for result in results:
        device_uuid = result.get("deviceUuid", "Unknown Device")

        # Match device UUID to hostname
        matched_device = next((d for d in devices if d["id"] == device_uuid), None)
        if matched_device:
            hostname = matched_device["hostname"]
        else:
            hostname = device_uuid

        # Get success or failure output
        success_output = result.get("commandResponses", {}).get("SUCCESS", {})
        failure_output = result.get("commandResponses", {}).get("FAILURE", {})

        print("==============================")
        print("DEVICE:", hostname)
        print("==============================\n")

        if "show ip int brief" in success_output:
            print(success_output["show ip int brief"])
        elif failure_output:
            print("Command failed:")
            print(failure_output)
        else:
            print("No output returned.")

        print("\n")


if __name__ == "__main__":
    main()

# References: https://developer.cisco.com/docs/catalyst-center/command-runner/#endpoints-and-methods-used
