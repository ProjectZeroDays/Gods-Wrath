from tkinter import Tk, Label, Entry, Button, messagebox
from audit_tool.database.setup_database import authenticate
import pyotp
import json
import os

# Load configuration
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "audit_tool")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
with open(CONFIG_PATH, "r") as config_file:
    config = json.load(config_file)

def login_gui():
    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        otp = otp_entry.get()
        if authenticate(username, password):
            totp = pyotp.TOTP(config["2fa_secret"])
            if totp.verify(otp):
                messagebox.showinfo("Login Success", "Welcome!")
            else:
                messagebox.showerror("Login Failed", "Invalid OTP")
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

    Label(root, text="OTP").grid(row=2, column=0)
    otp_entry = Entry(root)
    otp_entry.grid(row=2, column=1)

    Button(root, text="Login", command=on_login).grid(row=3, column=0, columnspan=2)

    root.mainloop()
