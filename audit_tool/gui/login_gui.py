from tkinter import Tk, Label, Entry, Button, messagebox
from audit_tool.database.setup_database import authenticate

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
