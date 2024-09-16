import os
import sqlite3
from audit_tool.encryption.encryption import encrypt_message

# Constants
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "audit_tool")
DATABASE_PATH = os.path.join(CONFIG_DIR, 'users.db')

def setup_database():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS api_keys (username TEXT, api_key TEXT)''')
    conn.commit()
    conn.close()

def add_admin_user():
    admin_user = encrypt_message("projectzero")
    admin_pass = encrypt_message("R0om2fb9!")
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (admin_user, admin_pass))
    conn.commit()
    conn.close()

def authenticate(username, password):
    encrypted_username = encrypt_message(username)
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (encrypted_username,))
    result = c.fetchone()
    conn.close()
    if result and decrypt_message(result[0]) == password:
        return True
    return False
