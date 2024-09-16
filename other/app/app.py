#!/usr/bin/env python3

import os
import subprocess
import shutil
import getpass
import tempfile
import urllib.request
import zipfile
import base64
from cryptography.fernet import Fernet
import sqlite3
import time
import smtplib
import requests
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import Tk, Label, Entry, Button, messagebox
import logging

# Constants
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "audit_tool")
TOOLS_DIR = os.path.join(tempfile.gettempdir(), "tools")
DATABASE_PATH = os.path.join(CONFIG_DIR, 'users.db')
SECRET_KEY_PATH = os.path.join(CONFIG_DIR, "secret.key")
GIT_REPO_DIR = os.path.join(tempfile.gettempdir(), "audit-tool")
DOCS_DIR = os.path.join(GIT_REPO_DIR, "docs")

# Logging setup
logging.basicConfig(filename=os.path.join(CONFIG_DIR, 'audit_tool.log'), level=logging.INFO)

# Encryption key generation and saving
def generate_key():
    key = Fernet.generate_key()
    with open(SECRET_KEY_PATH, "wb") as key_file:
        key_file.write(key)
    logging.info("Encryption key generated and saved.")

def load_key():
    return open(SECRET_KEY_PATH, "rb").read()

def encrypt_message(message):
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

# Base64 encoding
def encode_base64(text):
    return base64.b64encode(text.encode()).decode()

def decode_base64(encoded_text):
    return base64.b64decode(encoded_text.encode()).decode()

# Database setup
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

# Add admin user
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

# Authentication function
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

# Function to send email notification
def send_email(subject, body, to_email):
    try:
        from_email = "your_email@example.com"
        from_password = "your_password"
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        logging.info(f"Email sent to {to_email}.")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

# Function to send SMS notification
def send_sms(message, to_number):
    try:
        api_url = "https://sms-api.example.com/send"
        api_key = "your_sms_api_key"
        data = {
            "to": to_number,
            "message": message,
            "api_key": api_key
        }
        response = requests.post(api_url, data=data)
        if response.status_code == 200:
            logging.info(f"SMS sent to {to_number}.")
            return True
        else:
            logging.error(f"Error sending SMS: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Error sending SMS: {e}")
        return False

# Function to handle payment processing
def process_payment(amount):
    try:
        payment_url = "https://payment-gateway.example.com/process"
        data = {
            "amount": amount,
            "api_key": "your_payment_api_key"
        }
        response = requests.post(payment_url, data=data)
        logging.info(f"Payment processed: {response.json()}")
        return response.json()
    except Exception as e:
        logging.error(f"Error processing payment: {e}")
        return None

# GUI for user authentication
def login_gui():
    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        if authenticate(username, password):
            messagebox.showinfo("Login Success", "Welcome!")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    root = Tk()
    root.title("Login")

    Label(root, text="Username").grid(row=0, column=0)
    username_entry = Entry(root)
    username_entry.grid(row=0, column=1)

    Label(root, text="Password").grid(row=1, column=0)
    password_entry = Entry(root, show="*")
    password_entry.grid(row=1, column=1)

    Button(root, text="Login", command=on_login).grid(row=2, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    setup_database()
    add_admin_user()
    login_gui()
