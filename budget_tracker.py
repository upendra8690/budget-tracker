"""
SMART BUDGET TRACKER 💰
======================
A beginner-friendly but professional budget tracker.

Features:
✓ Add purchases (single / multiple)
✓ Discount calculator
✓ Transaction history
✓ Auto-save data (JSON file)
✓ Input validation (no crashing)
✓ Clear summary report
"""

import json
import os
from datetime import datetime


DATA_FILE = "budget_data.json"


# ========== HELPER FUNCTIONS ==========

def show_welcome():
    print("\n💰 SMART BUDGET TRACKER 💰")
    print("=" * 45)


def load_data():
    """Load budget data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"budget": 0.0, "spent": 0.0, "purchases": []}


def save_data(data):
    """Save budget data to JSON file"""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def safe_float_input(message):
    """Safely take float input (prevents crash)"""
    while True:
        try:
            value = float(input(message))
            return value
        except ValueError:
            print("❌ Invalid input. Enter a number only.")


def safe_int_input(message):
    """Safely take integer input"""
    while True:
        try:
            value = int(input(message))
            return value
        except ValueError:
            print("❌ Invalid input. Enter an integer only.")


def get_budget_status(budget, spent):
    remaining = budget - spent
    percentage = (spent / budget) * 100 if budget > 0 else 0

    print("\n📌 CURRENT STATUS")
    print("-" * 45)
    print(f"Budget      : ${budget:.2f}")
    print(f"Spent       : ${spent:.2f}")
    print(f"Remaining   : ${remaining:.2f}")
    print(f"Usage       : {percentage:.1f}% used")

    if remaining > budget * 0.5:
        print("Status      : ✅ Good (safe spending)")
    elif remaining > 0:
        print("Status      : ⚠ Careful (budget is tight)")
    else:
        print("Status      : ❌ Over Budget!")

    return remaining


def can_buy(price, remaining):
    return price > 0 and price <= remaining


def add_purchase(data, name, price):
    """Add purchase to history"""
    data["spent"] += price
    data["purchases"].append({
        "name": name,
        "price": price,
        "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    })


def show_history(data):
    """Display purchase history"""
    if len(data["purchases"]) == 0:
        print("\n📭 No purchases yet.")
        return

    print("\n🧾 PURCHASE HISTORY")
    print("=" * 45)

    for i, item in enumerate(data["purchases"], start=1):
        print(f"{i}. {item['name']} - ${item['price']:.2f} ({item['time']})")

    print("=" * 45)
    print(f"Total purchases: {len(data['purchases'])}")


def calculate_discount(price, discount_percent):
    discount = price * (discount_percent / 100)
    final_price = price - discount

    print("\n💸 DISCOUNT RESULT")
    print("-" * 45)
    print(f"Original Price : ${price:.2f}")
    print(f"Discount       : {discount_percent}% (-${discount:.2f})")
    print(f"Final Price    : ${final_price:.2f}")

    return final_price


# ========== MAIN PROGRAM ==========

def main():
    show_welcome()

    data = load_data()

    # If budget is not set, ask user
    if data["budget"] == 0:
        data["budget"] = safe_float_input("\nEnter your weekly budget: $")
        save_data(data)

    while True:
        remaining = get_budget_status(data["budget"], data["spent"])

        print("\n" + "=" * 45)
        print("MENU")
        print("=" * 45)
        print("1. Add a purchase")
        print("2. Buy multiple items")
        print("3. Discount calculator")
        print("4. View purchase history")
        print("5. Reset budget (new week)")
        print("6. Exit")
        print("=" * 45)

        choice = input("Choose option (1-6): ")

        # OPTION 1: Single Purchase
        if choice == "1":
            print("\n🛒 Add Purchase")
            name = input("Item name: ").strip()
            price = safe_float_input("Item price: $")

            if name == "":
                print("❌ Item name cannot be empty.")
                continue

            if can_buy(price, remaining):
                confirm = input(f"Confirm purchase of {name} for ${price:.2f}? (yes/no): ").lower()
                if confirm == "yes":
                    add_purchase(data, name, price)
                    save_data(data)
                    print("✅ Purchase added successfully!")
                else:
                    print("❌ Purchase cancelled.")
            else:
                print(f"❌ Not affordable. Need ${price - remaining:.2f} more.")

        # OPTION 2: Multiple Items
        elif choice == "2":
            print("\n📦 Multiple Items Mode")
            cart_total = 0.0
            cart_items = []

            while True:
                item_name = input("Enter item name (or 'done'): ").strip()

                if item_name.lower() == "done":
                    break

                if item_name == "":
                    print("❌ Empty name not allowed.")
                    continue

                item_price = safe_float_input(f"Price for {item_name}: $")

                if item_price <= 0:
                    print("❌ Invalid price.")
                    continue

                cart_items.append((item_name, item_price))
                cart_total += item_price
                print(f"✅ Added {item_name} (${item_price:.2f})")

            if len(cart_items) == 0:
                print("❌ No items added.")
                continue

            print(f"\n🧾 Cart Total = ${cart_total:.2f}")

            if cart_total <= remaining:
                confirm = input("Proceed with all purchases? (yes/no): ").lower()
                if confirm == "yes":
                    for name, price in cart_items:
                        add_purchase(data, name, price)
                    save_data(data)
                    print("✅ All items purchased successfully!")
                else:
                    print("❌ Cart cancelled.")
            else:
                print(f"❌ Can't afford cart. Need ${cart_total - remaining:.2f} more.")

        # OPTION 3: Discount calculator
        elif choice == "3":
            print("\n💸 Discount Calculator")
            price = safe_float_input("Original price: $")
            discount = safe_int_input("Discount %: ")

            if discount < 0 or discount > 100:
                print("❌ Discount must be between 0 and 100.")
                continue

            final_price = calculate_discount(price, discount)

            if can_buy(final_price, remaining):
                print("✅ You can afford it after discount.")
            else:
                print("❌ Still too expensive.")

        # OPTION 4: History
        elif choice == "4":
            show_history(data)

        # OPTION 5: Reset budget
        elif choice == "5":
            confirm = input("Reset budget and purchases for new week? (yes/no): ").lower()
            if confirm == "yes":
                data = {"budget": safe_float_input("Enter new weekly budget: $"), "spent": 0.0, "purchases": []}
                save_data(data)
                print("✅ New week started successfully!")

        # OPTION 6: Exit
        elif choice == "6":
            print("\n👋 Exiting Budget Tracker...")
            break

        else:
            print("❌ Invalid option. Choose between 1-6.")

    # FINAL SUMMARY
    print("\n" + "=" * 45)
    print("FINAL SUMMARY REPORT")
    print("=" * 45)
    print(f"Budget:    ${data['budget']:.2f}")
    print(f"Spent:     ${data['spent']:.2f}")
    print(f"Remaining: ${data['budget'] - data['spent']:.2f}")
    print(f"Purchases: {len(data['purchases'])}")
    print("=" * 45)


if __name__ == "__main__":
    main()
