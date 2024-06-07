import tkinter as tk
from tkinter import messagebox, simpledialog

#Secondary program - GUI

menu = {
    1: {"name": "All day (large)", "price": 5.50},
    2: {"name": "All day (small)", "price": 3.50},
    3: {"name": "Hot dog", "price": 3.00},
    4: {"name": "Burger", "price": 4.00},
    5: {"name": "Cheese burger", "price": 4.25},
    6: {"name": "Chicken goujons", "price": 3.50},
    7: {"name": "Fries", "price": 1.75},
    8: {"name": "Salad", "price": 2.20},
    9: {"name": "Milkshake", "price": 2.20},
    10: {"name": "Soft drinks", "price": 1.30},
    11: {"name": "Still water", "price": 0.90},
    12: {"name": "Sparkling water", "price": 0.90}
}

order_totals = 0.0
item_totals = {item: 0 for item in menu}

def save_to_file(filename, data):
    with open(filename, 'w') as file:
        for line in data:
            file.write(line + '\n')

def load_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        return []

def save_menu():
    data = [f"{key},{value['name']},{value['price']}" for key, value in menu.items()]
    save_to_file('menu.txt', data)

def load_menu():
    global menu
    lines = load_from_file('menu.txt')
    for line in lines:
        item_id, name, price = line.split(',')
        menu[int(item_id)] = {"name": name, "price": float(price)}

def save_totals():
    data = [str(order_totals)] + [f"{key},{value}" for key, value in item_totals.items()]
    save_to_file('totals.txt', data)

def load_totals():
    global order_totals, item_totals
    lines = load_from_file('totals.txt')
    if lines:
        order_totals = float(lines[0])
        item_totals = {int(item.split(',')[0]): int(item.split(',')[1]) for item in lines[1:]}

def display_menu():
    menu_text = "MENU\n"
    for key, value in menu.items():
        menu_text += f"{key}. {value['name']} £{value['price']:.2f}\n"
    messagebox.showinfo("Menu", menu_text)

def add_menu_item():
    global menu
    try:
        item_details = simpledialog.askstring("Add Menu Item", "Enter the new menu item (format: ID, name, price):")
        if item_details:
            item_id, name, price = item_details.split(", ")
            menu[int(item_id)] = {"name": name, "price": float(price)}
            save_menu()
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please use the format: ID, name, price")

def amend_menu_item():
    global menu
    display_menu()
    try:
        item_id = simpledialog.askinteger("Amend Menu Item", "Enter the item number to amend:")
        if item_id in menu:
            item_details = simpledialog.askstring("Amend Menu Item", f"Enter the new details (format: name, price) for {menu[item_id]['name']}:")
            if item_details:
                name, price = item_details.split(", ")
                menu[item_id] = {"name": name, "price": float(price)}
                save_menu()
        else:
            messagebox.showerror("Error", "Invalid item number.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please use the format: name, price")

def delete_menu_item():
    global menu
    display_menu()
    try:
        item_id = simpledialog.askinteger("Delete Menu Item", "Enter the item number to delete:")
        if item_id in menu:
            del menu[item_id]
            save_menu()
        else:
            messagebox.showerror("Error", "Invalid item number.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid item number.")

def process_order():
    global order_totals
    display_menu()
    try:
        order_input = simpledialog.askstring("Process Order", "Enter the order details (table number and item numbers separated by commas):")
        if order_input:
            order_input = order_input.split(", ")
            table_number = order_input[0]
            order_items = [int(item) for item in order_input[1:]]
            order_cost = 0.0

            order_summary = f"Order for table {table_number}:\n"
            for item in order_items:
                if item in menu:
                    item_totals[item] += 1
                    order_cost += menu[item]["price"]
                    order_summary += f"{menu[item]['name']} - £{menu[item]['price']:.2f}\n"
                else:
                    order_summary += f"Invalid item number: {item}\n"

            order_summary += f"\nTotal cost: £{order_cost:.2f}"
            messagebox.showinfo("Order Summary", order_summary)
            order_totals += order_cost
            save_totals()
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input. Please use the format: table number, item numbers separated by commas. Error: {e}")

def display_totals():
    totals_text = "Running totals of the quantity of each menu item ordered:\n"
    for item, count in item_totals.items():
        totals_text += f"{menu[item]['name']}: {count} ordered\n"
    totals_text += f"\nTotal order value: £{order_totals:.2f}"
    messagebox.showinfo("Running Totals", totals_text)

def main():
    load_menu()
    load_totals()

    root = tk.Tk()
    root.title("Restaurant Order Management")

    tk.Button(root, text="Display Menu", command=display_menu).pack(pady=5)
    tk.Button(root, text="Add Menu Item", command=add_menu_item).pack(pady=5)
    tk.Button(root, text="Amend Menu Item", command=amend_menu_item).pack(pady=5)
    tk.Button(root, text="Delete Menu Item", command=delete_menu_item).pack(pady=5)
    tk.Button(root, text="Process Order", command=process_order).pack(pady=5)
    tk.Button(root, text="Display Running Totals", command=display_totals).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
