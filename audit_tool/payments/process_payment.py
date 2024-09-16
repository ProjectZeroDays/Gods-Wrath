import requests
import json
import os

# Load configuration
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "audit_tool")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
with open(CONFIG_PATH, "r") as config_file:
    config = json.load(config_file)

def process_payment(amount):
    try:
        payment_url = config["payment_api_url"]
        data = {
            "amount": amount,
            "api_key": config["payment_api_key"]
        }
        response = requests.post(payment_url, data=data)
        return response.json()
    except Exception as e:
        print(f"Error processing payment: {e}")
        return None
