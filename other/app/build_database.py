#!/usr/bin/env python3

import os
import sqlite3
from cryptography.fernet import Fernet

# Constants
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "audit_tool")
DATABASE_PATH = os.path.join(CONFIG_DIR, 'users.db')
SECRET_KEY_PATH = os.path.join(CONFIG_DIR, "secret.key")

# Encryption key generation and saving
def generate_key():
    key = Fernet.generate_key()
    with open(SECRET_KEY_PATH, "wb") as key_file:
        key_file.write(key)

def load_key():
    return open(SECRET_KEY_PATH, "rb").read()

def encrypt_message(message):
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# Database setup
def setup_database():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS api_keys (username TEXT, api_key TEXT)''')
    conn.commit()
    conn.close()

# Add admin user
def add_admin_user():
    admin_user = encrypt_message("projectzero")
    admin_pass = encrypt_message("R0om2fb9!")
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (admin_user, admin_pass))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    generate_key()
    setup_database()
    add_admin_user()
