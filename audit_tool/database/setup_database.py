import os
import sqlite3
from audit_tool.encryption.encryption import encrypt_message, decrypt_message
import logging

# Constants
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "audit_tool")
DATABASE_PATH = os.path.join(CONFIG_DIR, 'users.db')

def setup_database():
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS api_keys (username TEXT, api_key TEXT)''')
        conn.commit()
        conn.close()
        logging.info("Database setup completed.")
    except Exception as e:
        logging.error(f"Error setting up database: {e}")

def add_admin_user():
    try:
        admin_user = encrypt_message("projectzero")
        admin_pass = encrypt_message("R0om2fb9!")
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (admin_user, admin_pass))
        conn.commit()
        conn.close()
        logging.info("Admin user added.")
    except Exception as e:
        logging.error(f"Error adding admin user: {e}")

def authenticate(username, password):
    try:
        encrypted_username = encrypt_message(username)
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (encrypted_username,))
        result = c.fetchone()
        conn.close()
        if result and decrypt_message(result[0]) == password:
            return True
        return False
    except Exception as e:
        logging.error(f"Error during authentication: {e}")
        return False
