import tkinter as tk
from tkinter import messagebox
import sqlite3

# ---------------- DATABASE ----------------

conn = sqlite3.connect("food_order.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food TEXT,
    price INTEGER
)
""")

conn.commit()

# ---------------- FOOD MENU ----------------

foods = {
    "Pizza": 199,
    "Burger": 129,
    "Veg Momos": 99,
    "Cheese Pizza": 249,
    "Samosa": 40,
    "Pasta": 159
}

cart = []

# ---------------- FUNCTIONS ----------------

def add_to_cart(food):
    cart.append((food, foods[food]))
    update_cart()
    messagebox.showinfo("Added", food + " added to cart!")


def remove_from_cart():
    selected = cart_list.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Please select an item.")
        return

    index = selected[0]
    cart.pop(index)

    update_cart()


def update_cart():

    cart_list.delete(0, tk.END)

    total = 0

    for food, price in cart:
        cart_list.insert(tk.END, food + " - ₹" + str(price))
        total += price

    total_label.config(text="Total: ₹" + str(total))


def place_order():

    if len(cart) == 0:
        messagebox.showwarning(
            "Empty Cart",
            "Please add food to cart first."
        )
        return

    for food, price in cart:

        cursor.execute(
            "INSERT INTO orders (food, price) VALUES (?, ?)",
            (food, price)
        )

    conn.commit()

    total = sum(price for food, price in cart)

    messagebox.showinfo(
        "Order Successful",
        "Order placed successfully!\n\nTotal: ₹" + str(total)
    )

    cart.clear()
    update_cart()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("Online Food Ordering System")
root.geometry("700x600")
root.config(bg="#f5f5f5")

title = tk.Label(
    root,
    text="🍔 ONLINE FOOD ORDERING SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#e63946",
    fg="white",
    pady=15
)

title.pack(fill="x")

# ---------------- MENU ----------------

menu_frame = tk.Frame(root, bg="#f5f5f5")
menu_frame.pack(pady=20)

tk.Label(
    menu_frame,
    text="FOOD MENU",
    font=("Arial", 18, "bold"),
    bg="#f5f5f5"
).grid(row=0, column=0, columnspan=2, pady=10)


row = 1

for food, price in foods.items():

    tk.Label(
        menu_frame,
        text=food + " - ₹" + str(price),
        font=("Arial", 13),
        bg="#f5f5f5"
    ).grid(row=row, column=0, padx=20, pady=5)

    tk.Button(
        menu_frame,
        text="Add to Cart",
        command=lambda f=food: add_to_cart(f),
        bg="#e63946",
        fg="white",
        width=15
    ).grid(row=row, column=1, padx=20, pady=5)

    row += 1


# ---------------- CART ----------------

cart_frame = tk.Frame(root, bg="white")
cart_frame.pack(pady=15, padx=30, fill="both")

tk.Label(
    cart_frame,
    text="🛒 YOUR CART",
    font=("Arial", 18, "bold"),
    bg="white"
).pack(pady=10)

cart_list = tk.Listbox(
    cart_frame,
    width=50,
    height=7,
    font=("Arial", 12)
)

cart_list.pack()

total_label = tk.Label(
    cart_frame,
    text="Total: ₹0",
    font=("Arial", 16, "bold"),
    bg="white"
)

total_label.pack(pady=10)


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Remove Item",
    command=remove_from_cart,
    bg="#ff9800",
    fg="white",
    width=15
).grid(row=0, column=0, padx=10)

tk.Button(
    button_frame,
    text="Place Order",
    command=place_order,
    bg="#28a745",
    fg="white",
    width=15
).grid(row=0, column=1, padx=10)


# ---------------- START ----------------

root.mainloop()