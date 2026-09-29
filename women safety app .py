import tkinter as tk
from tkinter import messagebox
import sqlite3
import webbrowser
import urllib.parse

# ---------------- DATABASE ----------------

conn = sqlite3.connect("safety_app.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    username TEXT,
    name TEXT,
    phone TEXT
)
""")

conn.commit()


# ---------------- REGISTER ----------------

def register():
    username = reg_user.get()
    password = reg_pass.get()

    if username == "" or password == "":
        messagebox.showwarning("Warning", "Please enter all details.")
        return

    try:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?)",
            (username, password)
        )
        conn.commit()

        messagebox.showinfo(
            "Success",
            "Registration successful!"
        )

        reg_user.delete(0, tk.END)
        reg_pass.delete(0, tk.END)

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Username already exists."
        )


# ---------------- LOGIN ----------------

def login():
    username = login_user.get()
    password = login_pass.get()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    result = cursor.fetchone()

    if result:
        login_window.destroy()
        open_dashboard(username)
    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )


# ---------------- ADD CONTACT ----------------

def add_contact(username, name_entry, phone_entry, listbox):

    name = name_entry.get()
    phone = phone_entry.get()

    if name == "" or phone == "":
        messagebox.showwarning(
            "Warning",
            "Enter contact name and phone number."
        )
        return

    cursor.execute(
        "INSERT INTO contacts VALUES (?, ?, ?)",
        (username, name, phone)
    )

    conn.commit()

    listbox.insert(
        tk.END,
        name + " - " + phone
    )

    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

    messagebox.showinfo(
        "Success",
        "Emergency contact added."
    )


# ---------------- LOAD CONTACTS ----------------

def load_contacts(username, listbox):

    cursor.execute(
        "SELECT name, phone FROM contacts WHERE username=?",
        (username,)
    )

    contacts = cursor.fetchall()

    for name, phone in contacts:
        listbox.insert(
            tk.END,
            name + " - " + phone
        )


# ---------------- SOS ----------------

def sos(username):

    cursor.execute(
        "SELECT name, phone FROM contacts WHERE username=?",
        (username,)
    )

    contacts = cursor.fetchall()

    if not contacts:
        messagebox.showwarning(
            "No Contact",
            "Please add an emergency contact first."
        )
        return

    message = (
        "EMERGENCY! I need help. "
        "Please contact me immediately."
    )

    encoded_message = urllib.parse.quote(message)

    webbrowser.open(
        "https://wa.me/?text=" + encoded_message
    )

    messagebox.showinfo(
        "SOS",
        "Emergency message prepared in WhatsApp."
    )


# ---------------- LOCATION ----------------

def open_location():

    webbrowser.open(
        "https://maps.google.com"
    )

    messagebox.showinfo(
        "Location",
        "Google Maps opened. "
        "You can share your current location."
    )


# ---------------- SAFETY TIPS ----------------

def safety_tips():

    tips = """
WOMEN SAFETY TIPS

1. Keep your phone charged.
2. Save trusted emergency contacts.
3. Tell someone you trust about your travel plans.
4. Avoid isolated places when possible.
5. Keep your emergency contacts updated.
6. Share your location with a trusted person when needed.
7. In an emergency, contact local emergency services.
"""

    messagebox.showinfo(
        "Safety Tips",
        tips
    )


# ---------------- EMERGENCY NUMBERS ----------------

def emergency_numbers():

    numbers = """
IMPORTANT EMERGENCY NUMBERS

Police: 112
Women Helpline: 181
Ambulance: 108
"""

    messagebox.showinfo(
        "Emergency Numbers",
        numbers
    )


# ---------------- DASHBOARD ----------------

def open_dashboard(username):

    dashboard = tk.Tk()
    dashboard.title("Women Safety Dashboard")
    dashboard.geometry("600x700")

    title = tk.Label(
        dashboard,
        text="WOMEN SAFETY APP",
        font=("Arial", 24, "bold")
    )

    title.pack(pady=20)

    welcome = tk.Label(
        dashboard,
        text="Welcome, " + username,
        font=("Arial", 15)
    )

    welcome.pack(pady=5)

    # Emergency contacts

    tk.Label(
        dashboard,
        text="Emergency Contacts",
        font=("Arial", 15, "bold")
    ).pack(pady=10)

    name_entry = tk.Entry(
        dashboard,
        width=35
    )
    name_entry.pack(pady=5)
    name_entry.insert(0, "Contact Name")

    phone_entry = tk.Entry(
        dashboard,
        width=35
    )
    phone_entry.pack(pady=5)
    phone_entry.insert(0, "Phone Number")

    contact_list = tk.Listbox(
        dashboard,
        width=45,
        height=6
    )
    contact_list.pack(pady=10)

    load_contacts(
        username,
        contact_list
    )

    tk.Button(
        dashboard,
        text="Add Emergency Contact",
        width=25,
        command=lambda: add_contact(
            username,
            name_entry,
            phone_entry,
            contact_list
        )
    ).pack(pady=8)

    # SOS

    tk.Button(
        dashboard,
        text="🚨 EMERGENCY SOS",
        bg="red",
        fg="white",
        font=("Arial", 17, "bold"),
        width=25,
        height=2,
        command=lambda: sos(username)
    ).pack(pady=20)

    # Location

    tk.Button(
        dashboard,
        text="📍 Open Location",
        width=25,
        height=2,
        command=open_location
    ).pack(pady=8)

    # Safety tips

    tk.Button(
        dashboard,
        text="🛡 Safety Tips",
        width=25,
        height=2,
        command=safety_tips
    ).pack(pady=8)

    # Emergency numbers

    tk.Button(
        dashboard,
        text="☎ Emergency Numbers",
        width=25,
        height=2,
        command=emergency_numbers
    ).pack(pady=8)

    dashboard.mainloop()


# ---------------- LOGIN WINDOW ----------------

login_window = tk.Tk()
login_window.title("Women Safety App - Login")
login_window.geometry("500x550")

tk.Label(
    login_window,
    text="WOMEN SAFETY APP",
    font=("Arial", 24, "bold")
).pack(pady=25)

# Login

tk.Label(
    login_window,
    text="LOGIN",
    font=("Arial", 18, "bold")
).pack(pady=10)

login_user = tk.Entry(
    login_window,
    width=35
)
login_user.pack(pady=5)

login_pass = tk.Entry(
    login_window,
    width=35,
    show="*"
)
login_pass.pack(pady=5)

tk.Button(
    login_window,
    text="LOGIN",
    width=20,
    command=login
).pack(pady=15)


# Register

tk.Label(
    login_window,
    text="REGISTER NEW USER",
    font=("Arial", 16, "bold")
).pack(pady=15)

reg_user = tk.Entry(
    login_window,
    width=35
)
reg_user.pack(pady=5)

reg_pass = tk.Entry(
    login_window,
    width=35,
    show="*"
)
reg_pass.pack(pady=5)

tk.Button(
    login_window,
    text="REGISTER",
    width=20,
    command=register
).pack(pady=15)

login_window.mainloop()

conn.close()