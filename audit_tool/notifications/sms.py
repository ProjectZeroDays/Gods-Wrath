import requests
import json
import os
import logging

# Load configuration
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "audit_tool")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
with open(CONFIG_PATH, "r") as config_file:
    config = json.load(config_file)

def send_sms(message, to_number):
    try:
        api_url = config["sms_api_url"]
        api_key = config["sms_api_key"]
        data = {
            "to": to_number,
            "message": message,
            "api_key": api_key
        }
        response = requests.post(api_url, data=data)
        if response.status_code == 200:
            logging.info(f"SMS sent to {to_number}.")
            return True
