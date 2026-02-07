"""
🚀 ULTRA SMART BUDGET TRACKER 💰
================================
A real-world beginner project that feels professional.

Features:
✅ Add purchase with category
✅ Multiple items cart
✅ Discount calculator
✅ Auto-save JSON file
✅ View purchase history
✅ Category summary
✅ Delete purchase
✅ Edit purchase
✅ Search purchase
✅ Top 5 expensive purchases
✅ Spending bar chart (terminal)
✅ Export purchases to CSV file
✅ Backup JSON data
✅ Budget warning alerts
✅ Reset week

Author: Upendra Reddy
"""

import json
import os
import csv
from datetime import datetime

DATA_FILE = "budget_data.json"
EXPORT_FILE = "budget_export.csv"


# ================= BASIC FUNCTIONS =================

def show_welcome():
    print("\n🚀 ULTRA SMART BUDGET TRACKER 💰")
    print("=" * 65)


def safe_float_input(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("❌ Invalid input. Enter only numbers.")


def safe_int_input(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("❌ Invalid input. Enter only integers.")


# ================= FILE FUNCTIONS =================

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("⚠ Data corrupted! Creating fresh file...")
            return {"budget": 0.0, "spent": 0.0, "purchases": []}
    return {"budget": 0.0, "spent": 0.0, "purchases": []}


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def backup_data():
    if not os.path.exists(DATA_FILE):
        print("❌ No data file found to backup.")
        return

    backup_name = f"backup_{datetime.now().strftime('%d%m%Y_%H%M%S')}.json"

    with open(DATA_FILE, "r") as original:
        content = original.read()

    with open(backup_name, "w") as backup:
        backup.write(content)

    print(f"✅ Backup created: {backup_name}")


# ================= PURCHASE FUNCTIONS =================

def can_buy(price, remaining):
    return price > 0 and price <= remaining


def add_purchase(data, name, category, price):
    data["spent"] += price
    data["purchases"].append({
        "name": name,
        "category": category,
        "price": price,
        "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    })


def delete_purchase(data):
    if len(data["purchases"]) == 0:
        print("\n📭 No purchases to delete.")
        return

    show_history(data)

    index = safe_int_input("\nEnter purchase number to delete: ")

    if index < 1 or index > len(data["purchases"]):
        print("❌ Invalid purchase number.")
        return

    removed_item = data["purchases"].pop(index - 1)
    data["spent"] -= removed_item["price"]
    save_data(data)

    print(f"✅ Deleted: {removed_item['name']} (${removed_item['price']:.2f})")


def edit_purchase(data):
    if len(data["purchases"]) == 0:
        print("\n📭 No purchases to edit.")
        return

    show_history(data)

    index = safe_int_input("\nEnter purchase number to edit: ")

    if index < 1 or index > len(data["purchases"]):
        print("❌ Invalid purchase number.")
        return

    item = data["purchases"][index - 1]

    print("\n✏ EDIT MODE")
    print("-" * 65)
    print(f"Current Name     : {item['name']}")
    print(f"Current Category : {item['category']}")
    print(f"Current Price    : ${item['price']:.2f}")
    print("-" * 65)

    new_name = input("New name (press Enter to keep same): ").strip()
    new_category = input("New category (press Enter to keep same): ").strip()
    new_price_input = input("New price (press Enter to keep same): ").strip()

    old_price = item["price"]

    if new_name != "":
        item["name"] = new_name

    if new_category != "":
        item["category"] = new_category

    if new_price_input != "":
        try:
            new_price = float(new_price_input)
            if new_price <= 0:
                print("❌ Price must be greater than 0.")
                return
            item["price"] = new_price
        except ValueError:
            print("❌ Invalid price entered.")
            return

    # Update total spent correctly
    data["spent"] = data["spent"] - old_price + item["price"]

    save_data(data)
    print("✅ Purchase updated successfully!")


def search_purchase(data):
    if len(data["purchases"]) == 0:
        print("\n📭 No purchases available.")
        return

    keyword = input("\nEnter keyword to search (name/category): ").lower().strip()

    if keyword == "":
        print("❌ Search keyword cannot be empty.")
        return

    found = False
    print("\n🔍 SEARCH RESULTS")
    print("=" * 65)

    for i, item in enumerate(data["purchases"], start=1):
        if keyword in item["name"].lower() or keyword in item["category"].lower():
            print(f"{i}. {item['name']} | {item['category']} | ${item['price']:.2f}")
            print(f"   Time: {item['time']}")
            found = True

    if not found:
        print("❌ No matching results found.")

    print("=" * 65)


# ================= DISPLAY FUNCTIONS =================

def get_budget_status(budget, spent):
    remaining = budget - spent
    percent_used = (spent / budget) * 100 if budget > 0 else 0

    print("\n📌 CURRENT STATUS")
    print("-" * 65)
    print(f"Weekly Budget     : ${budget:.2f}")
    print(f"Total Spent       : ${spent:.2f}")
    print(f"Remaining Money   : ${remaining:.2f}")
    print(f"Usage Percentage  : {percent_used:.1f}%")

    if percent_used < 50:
        print("Status            : ✅ Excellent (Saver Mode)")
    elif percent_used < 80:
        print("Status            : ⚠ Careful (Moderate Spending)")
    elif percent_used <= 100:
        print("Status            : 🚨 Warning! Budget Almost Finished!")
    else:
        print("Status            : ❌ Over Budget!")

    return remaining


def show_history(data):
    if len(data["purchases"]) == 0:
        print("\n📭 No purchases yet.")
        return

    print("\n🧾 PURCHASE HISTORY")
    print("=" * 65)

    for i, item in enumerate(data["purchases"], start=1):
        print(f"{i}. {item['name']} | {item['category']} | ${item['price']:.2f}")
        print(f"   Time: {item['time']}")

    print("=" * 65)
    print(f"Total Purchases: {len(data['purchases'])}")


def show_category_summary(data):
    if len(data["purchases"]) == 0:
        print("\n📭 No purchases yet.")
        return

    summary = {}

    for item in data["purchases"]:
        cat = item["category"]
        summary[cat] = summary.get(cat, 0) + item["price"]

    print("\n📊 CATEGORY SUMMARY")
    print("=" * 65)

    for cat, total in summary.items():
        print(f"{cat:<20} : ${total:.2f}")

    print("=" * 65)


def top_expensive(data):
    if len(data["purchases"]) == 0:
        print("\n📭 No purchases available.")
        return

    sorted_items = sorted(data["purchases"], key=lambda x: x["price"], reverse=True)

    print("\n🔥 TOP 5 EXPENSIVE PURCHASES")
    print("=" * 65)

    for i, item in enumerate(sorted_items[:5], start=1):
        print(f"{i}. {item['name']} | {item['category']} | ${item['price']:.2f}")

    print("=" * 65)


def show_spending_chart(data):
    if len(data["purchases"]) == 0:
        print("\n📭 No purchases available.")
        return

    summary = {}

    for item in data["purchases"]:
        cat = item["category"]
        summary[cat] = summary.get(cat, 0) + item["price"]

    max_spent = max(summary.values())

    print("\n📊 SPENDING BAR CHART (Category Wise)")
    print("=" * 65)

    for cat, total in summary.items():
        bar_length = int((total / max_spent) * 30)
        bar = "█" * bar_length
        print(f"{cat:<15} | {bar:<30} ${total:.2f}")

    print("=" * 65)


def export_to_csv(data):
    if len(data["purchases"]) == 0:
        print("\n📭 No purchases to export.")
        return

    with open(EXPORT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["No", "Item Name", "Category", "Price", "Time"])

        for i, item in enumerate(data["purchases"], start=1):
            writer.writerow([i, item["name"], item["category"], item["price"], item["time"]])

    print(f"✅ Exported successfully to {EXPORT_FILE}")


def calculate_discount(price, discount_percent):
    discount = price * (discount_percent / 100)
    final_price = price - discount

    print("\n💸 DISCOUNT RESULT")
    print("-" * 65)
    print(f"Original Price : ${price:.2f}")
    print(f"Discount       : {discount_percent}% (-${discount:.2f})")
    print(f"Final Price    : ${final_price:.2f}")

    return final_price


# ================= MAIN PROGRAM =================

def main():
    show_welcome()

    data = load_data()

    if data["budget"] <= 0:
        print("\n⚡ First time setup")
        data["budget"] = safe_float_input("Enter your weekly budget: $")
        save_data(data)

    while True:
        remaining = get_budget_status(data["budget"], data["spent"])

        print("\n" + "=" * 65)
        print("MENU")
        print("=" * 65)
        print("1. Add purchase")
        print("2. Buy multiple items")
        print("3. Discount calculator")
        print("4. View purchase history")
        print("5. Category summary")
        print("6. Delete purchase")
        print("7. Edit purchase")
        print("8. Search purchase")
        print("9. Top 5 expensive purchases")
        print("10. Spending bar chart")
        print("11. Export to CSV")
        print("12. Backup data")
        print("13. Reset week")
        print("14. Exit")
        print("=" * 65)

        choice = input("Choose option (1-14): ").strip()

        if choice == "1":
            print("\n🛒 ADD PURCHASE")
            name = input("Item name: ").strip()
            category = input("Category (Food/Travel/Shopping/etc): ").strip()

            if name == "" or category == "":
                print("❌ Name and category cannot be empty.")
                continue

            price = safe_float_input("Item price: $")

            if can_buy(price, remaining):
                confirm = input(f"Confirm purchase of {name} for ${price:.2f}? (yes/no): ").lower()
                if confirm == "yes":
                    add_purchase(data, name, category, price)
                    save_data(data)
                    print("✅ Purchase saved successfully!")
                else:
                    print("❌ Cancelled.")
            else:
                print(f"❌ Not affordable. Need ${price - remaining:.2f} more.")

        elif choice == "2":
            print("\n📦 MULTIPLE ITEMS MODE")
            cart_total = 0
            cart_items = []

            while True:
                item_name = input("Item name (or 'done'): ").strip()
                if item_name.lower() == "done":
                    break

                if item_name == "":
                    print("❌ Empty name not allowed.")
                    continue

                category = input("Category: ").strip()
                if category == "":
                    print("❌ Category required.")
                    continue

                item_price = safe_float_input(f"Price for {item_name}: $")

                if item_price <= 0:
                    print("❌ Invalid price.")
                    continue

                cart_items.append((item_name, category, item_price))
                cart_total += item_price
                print(f"✅ Added {item_name} (${item_price:.2f})")

            if len(cart_items) == 0:
                print("❌ No items added.")
                continue

            print(f"\n🧾 Cart Total = ${cart_total:.2f}")

            if cart_total <= remaining:
                confirm = input("Proceed with purchase? (yes/no): ").lower()
                if confirm == "yes":
                    for name, cat, price in cart_items:
                        add_purchase(data, name, cat, price)
                    save_data(data)
                    print("✅ Cart purchased successfully!")
                else:
                    print("❌ Cart cancelled.")
            else:
                print(f"❌ Can't afford cart. Need ${cart_total - remaining:.2f} more.")

        elif choice == "3":
            print("\n💸 DISCOUNT CALCULATOR")
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

        elif choice == "4":
            show_history(data)

        elif choice == "5":
            show_category_summary(data)

        elif choice == "6":
            delete_purchase(data)

        elif choice == "7":
            edit_purchase(data)

        elif choice == "8":
            search_purchase(data)

        elif choice == "9":
            top_expensive(data)

        elif choice == "10":
            show_spending_chart(data)

        elif choice == "11":
            export_to_csv(data)

        elif choice == "12":
            backup_data()

        elif choice == "13":
            confirm = input("Reset purchases and start new week? (yes/no): ").lower()
            if confirm == "yes":
                data = {"budget": safe_float_input("Enter new weekly budget: $"), "spent": 0.0, "purchases": []}
                save_data(data)
                print("✅ New week started!")

        elif choice == "14":
            print("\n👋 Exiting Budget Tracker...")
            break

        else:
            print("❌ Invalid option. Choose between 1-14.")

    print("\n" + "=" * 65)
    print("FINAL SUMMARY REPORT")
    print("=" * 65)
    print(f"Budget    : ${data['budget']:.2f}")
    print(f"Spent     : ${data['spent']:.2f}")
    print(f"Remaining : ${data['budget'] - data['spent']:.2f}")
    print(f"Purchases : {len(data['purchases'])}")
    print("=" * 65)


if __name__ == "__main__":
    main()
