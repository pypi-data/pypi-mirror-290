import os
import requests
from datetime import datetime, timedelta


# Fetch the list of all firewalla boxes in MSP tenant
def get_all_boxes(api_baseurl, api_token):
    headers = { "Authorization": f"Token {api_token}" }
    try:
        response = requests.get(f"{api_baseurl}/v2/boxes", headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching boxes: {e}")
        return None, f"Error fetching boxes: {e}"


# Fetch the list of devices for a specific box (using GID)
def get_fw_box_devices(api_baseurl, api_token, box_id):
    headers = { "Authorization": f"Token {api_token}" }
    try:
        response = requests.get(f"{api_baseurl}/v2/devices?box={box_id}", headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching devices: {e}")
        return None, f"Error fetching devices: {e}"



