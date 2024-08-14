import os
import requests
from datetime import datetime, timedelta

#####################################################################
# API config
# Must set FIREWALLA_API_TOKEN in host OS environment variables
#####################################################################
FW_API_BASEURL = '' # Set to FW MSP domain
FW_API_TOKEN = os.getenv('FIREWALLA_API_TOKEN')
REQ_HEADERS = { "Authorization": f"Token {FW_API_TOKEN}" }


# Verify required variables are set
def check_vars():
    if not all([FW_API_BASEURL, FW_API_TOKEN]):
        raise Exception("One or more required variables are not set.")
    
check_vars()

#####################################################################
# Main API functions
#####################################################################
# Fetch the list of all firewalla boxes in MSP tenant
def get_all_boxes():
    try:
        response = requests.get(f"{FW_API_BASEURL}/v2/boxes", headers=REQ_HEADERS)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching boxes: {e}")
        return None, f"Error fetching boxes: {e}"


# Fetch the list of devices for a specific box (using GID)
def get_fw_box_devices(fw_box_id):
    try:
        response = requests.get(f"{msp_domain}/v2/devices?box={fw_box_id}", headers=REQ_HEADERS)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching devices: {e}")
        return None, f"Error fetching devices: {e}"



