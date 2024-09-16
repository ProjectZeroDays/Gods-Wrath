import os
from cryptography.fernet import Fernet
import logging

# Constants
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "audit_tool")
SECRET_KEY_PATH = os.path.join(CONFIG_DIR, "secret.key")

def generate_key():
    try:
        key = Fernet.generate_key()
        with open(SECRET_KEY_PATH, "wb") as key_file:
            key_file.write(key)
        logging.info("Encryption key generated and saved.")
    except Exception as e:
        logging.error(f"Error generating encryption key: {e}")

def load_key():
    try:
        return open(SECRET_KEY_PATH, "rb").read()
    except Exception as e:
        logging.error(f"Error loading encryption key: {e}")
        return None

def encrypt_message(message):
    try:
        key = load_key()
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode())
        return encrypted_message
    except Exception as e:
        logging.error(f"Error encrypting message: {e}")
        return None

def decrypt_message(encrypted_message):
    try:
        key = load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message).decode()
        return decrypted_message
    except Exception as e:
        logging.error(f"Error decrypting message: {e}")
        return None
