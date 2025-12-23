import json
import uuid
from datetime import datetime

# ---------------- LOAD MENU ----------------
def load_menu():
    with open("menu.json", "r") as file:
        return json.load(file)

# ---------------- DISPLAY MENU ----------------
def display_menu(menu):
    print("\n🍽️ MENU 🍽️")
    for category, items in menu.items():
        print(f"\n{category}:")
        for item_id, details in items.items():
            print(f"  [{item_id}] {details['name']} - ₹{details['price']}")

# ---------------- FOOD ORDER CLASS ----------------
class FoodOrder:
    def __init__(self):
        self.order_id = str(uuid.uuid4())[:8]
        self.items = {}
        self.total = 0
        self.time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def add_item(self, name, price, qty):
        if name in self.items:
            self.items[name]["qty"] += qty
            self.items[name]["cost"] += price * qty
        else:
            self.items[name] = {
                "qty": qty,
                "cost": price * qty
            }
        self.total += price * qty

    def show_bill(self):
        print("\n🧾 FINAL BILL")
        for name, details in self.items.items():
            print(f"{name} x {details['qty']} = ₹{details['cost']}")
        print("----------------------------")
        print(f"Total Amount: ₹{self.total}")

# ---------------- SAVE ORDER ----------------
def save_order(order):
    with open("orders.txt", "a") as file:
        file.write(f"\nOrder ID: {order.order_id}\n")
        file.write(f"Time: {order.time}\n")
        file.write("Items:\n")
        for name, details in order.items.items():
            file.write(f"{name} x {details['qty']} = ₹{details['cost']}\n")
        file.write(f"Total: ₹{order.total}\n")
        file.write("------------------------------\n")

# ---------------- FIND ITEM BY ID ----------------
def find_item(menu, item_id):
    for category in menu.values():
        if item_id in category:
            return category[item_id]
    return None

# ---------------- TAKE ORDER ----------------
def take_order(menu, order):
    while True:
        choice = input("\nEnter item number (or 0 to finish): ")

        if choice == "0":
            break

        item = find_item(menu, choice)

        if item:
            try:
                qty = int(input("Enter quantity: "))
                if qty <= 0:
                    print("❌ Quantity must be greater than 0")
                    continue
                order.add_item(item["name"], item["price"], qty)
                print("✔ Item added to cart")
            except ValueError:
                print("❌ Please enter a valid number")
        else:
            print("❌ Invalid item number")

# ---------------- MAIN FUNCTION ----------------
def main():
    menu = load_menu()
    order = FoodOrder()

    print("PYTHON FOOD DELIVERY APPLICATION ")
    display_menu(menu)
    take_order(menu, order)

    if order.total == 0:
        print("\nNo items ordered.")
    else:
        order.show_bill()
        save_order(order)
        print("\n🙏 Thank you for ordering!")
        print("Your Order ID:", order.order_id)

if __name__ == "__main__":
    main()
