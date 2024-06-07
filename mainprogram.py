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

def save_menu():
    with open('menu.txt', 'w') as file:
        for key, value in menu.items():
            file.write(f"{key},{value['name']},{value['price']}\n")

def load_menu():
    global menu
    try:
        with open('menu.txt', 'r') as file:
            menu = {}
            for line in file:
                item_id, name, price = line.strip().split(',')
                menu[int(item_id)] = {"name": name, "price": float(price)}
    except FileNotFoundError:
        save_menu()

def save_totals():
    with open('totals.txt', 'w') as file:
        file.write(f"{order_totals}\n")
        for key, value in item_totals.items():
            file.write(f"{key},{value}\n")

def load_totals():
    global order_totals, item_totals
    try:
        with open('totals.txt', 'r') as file:
            order_totals = float(file.readline().strip())
            item_totals = {}
            for line in file:
                item_id, count = line.strip().split(',')
                item_totals[int(item_id)] = int(count)
    except FileNotFoundError:
        save_totals()

def display_menu():
    print("MENU")
    for key, value in menu.items():
        print(f"{key}. {value['name']} £{value['price']:.2f}")

def add_menu_item():
    global menu
    try:
        inputs = input("Enter the new menu item (format: ID, name, price): ").split(", ")
        item_id, name, price = int(inputs[0]), inputs[1], float(inputs[2])
        menu[item_id] = {"name": name, "price": price}
        save_menu()
    except ValueError:
        print("Invalid input. Please use the format: ID, name, price")

def amend_menu_item():
    global menu
    display_menu()
    try:
        item_id = int(input("Enter the item number to amend: "))
        if item_id in menu:
            inputs = input(f"Enter the new details (format: name, price) for {menu[item_id]['name']}: ").split(", ")
            name, price = inputs[0], float(inputs[1])
            menu[item_id] = {"name": name, "price": price}
            save_menu()
        else:
            print("Invalid item number.")
    except ValueError:
        print("Invalid input. Please use the format: name, price")

def delete_menu_item():
    global menu
    display_menu()
    try:
        item_id = int(input("Enter the item number to delete: "))
        if item_id in menu:
            del menu[item_id]
            save_menu()
        else:
            print("Invalid item number.")
    except ValueError:
        print("Invalid input. Please enter a valid item number.")

def process_order():
    global order_totals
    display_menu()
    try:
        order_input = input("Enter the order details (table number and item numbers separated by commas): ").split(", ")
        table_number = order_input[0]
        order_items = [int(item) for item in order_input[1:]]
        order_cost = 0.0

        print(f"Order for table {table_number}:")
        for item in order_items:
            print(f"Processing item: {item}")
            if item in menu:
                item_totals[item] += 1
                order_cost += menu[item]["price"]
                print(f"{menu[item]['name']} - £{menu[item]['price']:.2f}")
            else:
                print(f"Invalid item number: {item}")

        print(f"Total cost: £{order_cost:.2f}")
        order_totals += order_cost
        save_totals()
    except ValueError as e:
        print(f"Invalid input. Please use the format: table number, item numbers separated by commas. Error: {e}")

def display_totals():
    print("Running totals of the quantity of each menu item ordered:")
    for item, count in item_totals.items():
        print(f"{menu[item]['name']}: {count} ordered")

    print(f"\nTotal order value: £{order_totals:.2f}")

def main():
    load_menu()
    load_totals()
    while True:
        print("\n1. Display Menu")
        print("2. Add Menu Item")
        print("3. Amend Menu Item")
        print("4. Delete Menu Item")
        print("5. Process Order")
        print("6. Display Running Totals")
        print("7. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            display_menu()
        elif choice == "2":
            add_menu_item()
        elif choice == "3":
            amend_menu_item()
        elif choice == "4":
            delete_menu_item()
        elif choice == "5":
            process_order()
        elif choice == "6":
            display_totals()
        elif choice == "7":
            save_totals()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
