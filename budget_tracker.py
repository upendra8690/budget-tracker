"""
🚀 ULTRA SMART BUDGET TRACKER PRO MAX 💰
========================================
Professional CLI Budget Tracker (Company-Level Style)

🔥 Features:
✅ Add purchase with unique ID
✅ Cart purchase system
✅ Discount calculator
✅ Edit / Delete / Search purchase
✅ Undo last delete (rare feature)
✅ Sort purchases by price/date/category
✅ Category summary + spending chart
✅ Daily spending report
✅ Top 5 expensive purchases
✅ Analytics dashboard + prediction
✅ Export purchases to CSV + JSON
✅ Backup system (timestamped backup)
✅ Reset week system
✅ Safe auto-save JSON (prevents corruption)

Author: Upendra Reddy
"""

import json
import os
import csv
import uuid
from datetime import datetime
from typing import Dict, List, Any


# ================== CONSTANTS ==================
DATA_FILE = "budget_data.json"
EXPORT_CSV = "budget_export.csv"
EXPORT_JSON = "budget_export.json"


# ================== COLORS ==================
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# ================== UTILITIES ==================
def divider(length: int = 95) -> None:
    print("=" * length)


def now_time() -> str:
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def parse_time(time_string: str) -> datetime:
    return datetime.strptime(time_string, "%d-%m-%Y %H:%M:%S")


def safe_float_input(message: str) -> float:
    while True:
        try:
            value = float(input(message))
            return value
        except ValueError:
            print(f"{Colors.RED}❌ Invalid input. Enter numbers only.{Colors.RESET}")


def safe_int_input(message: str) -> int:
    while True:
        try:
            value = int(input(message))
            return value
        except ValueError:
            print(f"{Colors.RED}❌ Invalid input. Enter integers only.{Colors.RESET}")


def safe_non_empty(message: str) -> str:
    while True:
        value = input(message).strip()
        if value:
            return value
        print(f"{Colors.RED}❌ Input cannot be empty.{Colors.RESET}")


def calculate_total_spent(purchases: List[Dict[str, Any]]) -> float:
    return sum(item["price"] for item in purchases)


# ================== SAFE FILE SYSTEM ==================
def safe_write_json(filename: str, data: Dict[str, Any]) -> None:
    """
    Company-level safe write:
    Writes to a temp file first, then replaces the real file.
    Prevents file corruption during crashes.
    """
    temp_file = filename + ".tmp"
    with open(temp_file, "w") as file:
        json.dump(data, file, indent=4)
    os.replace(temp_file, filename)


def load_data() -> Dict[str, Any]:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

            data.setdefault("budget", 0.0)
            data.setdefault("purchases", [])
            data.setdefault("last_deleted", None)

            data["spent"] = calculate_total_spent(data["purchases"])
            return data

        except json.JSONDecodeError:
            print(f"{Colors.YELLOW}⚠ Data corrupted! Creating fresh file...{Colors.RESET}")

    return {"budget": 0.0, "spent": 0.0, "purchases": [], "last_deleted": None}


def save_data(data: Dict[str, Any]) -> None:
    data["spent"] = calculate_total_spent(data["purchases"])
    safe_write_json(DATA_FILE, data)


def backup_data() -> None:
    if not os.path.exists(DATA_FILE):
        print(f"{Colors.RED}❌ No data file found to backup.{Colors.RESET}")
        return

    backup_name = f"backup_{datetime.now().strftime('%d%m%Y_%H%M%S')}.json"

    with open(DATA_FILE, "r") as original:
        content = original.read()

    with open(backup_name, "w") as backup:
        backup.write(content)

    print(f"{Colors.GREEN}✅ Backup created successfully: {backup_name}{Colors.RESET}")


# ================== DISPLAY ==================
def show_welcome() -> None:
    print(f"\n{Colors.CYAN}{Colors.BOLD}🚀 ULTRA SMART BUDGET TRACKER PRO MAX 💰{Colors.RESET}")
    divider()
    print(f"{Colors.BLUE}Professional CLI Budget Management System (Company Style Project){Colors.RESET}")
    divider()


def budget_status(data: Dict[str, Any]) -> float:
    budget = data["budget"]
    spent = data["spent"]
    remaining = budget - spent
    percent_used = (spent / budget) * 100 if budget > 0 else 0

    print(f"\n{Colors.CYAN}{Colors.BOLD}📌 CURRENT STATUS DASHBOARD{Colors.RESET}")
    divider()
    print(f"Weekly Budget       : ${budget:.2f}")
    print(f"Total Spent         : ${spent:.2f}")
    print(f"Remaining Money     : ${remaining:.2f}")
    print(f"Usage Percentage    : {percent_used:.1f}%")
    divider()

    if percent_used < 50:
        print(f"{Colors.GREEN}Status: ✅ Excellent (Saver Mode){Colors.RESET}")
    elif percent_used < 80:
        print(f"{Colors.YELLOW}Status: ⚠ Moderate Spending{Colors.RESET}")
    elif percent_used <= 100:
        print(f"{Colors.YELLOW}Status: 🚨 Warning! Budget Almost Finished{Colors.RESET}")
    else:
        print(f"{Colors.RED}Status: ❌ Over Budget!{Colors.RESET}")

    return remaining


def show_history(data: Dict[str, Any]) -> None:
    purchases = data["purchases"]

    if not purchases:
        print(f"{Colors.YELLOW}📭 No purchases found.{Colors.RESET}")
        return

    print(f"\n{Colors.CYAN}{Colors.BOLD}🧾 PURCHASE HISTORY{Colors.RESET}")
    divider()

    for i, item in enumerate(purchases, start=1):
        print(f"{Colors.BOLD}{i}. {item['name']}{Colors.RESET} | {item['category']} | ${item['price']:.2f}")
        print(f"   ID: {item['id']} | 🕒 {item['time']}")

    divider()
    print(f"{Colors.BLUE}Total Purchases: {len(purchases)}{Colors.RESET}")


# ================== PURCHASE MANAGEMENT ==================
def can_buy(price: float, remaining: float) -> bool:
    return price > 0 and price <= remaining


def add_purchase(data: Dict[str, Any], name: str, category: str, price: float) -> None:
    data["purchases"].append({
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "category": category.title(),
        "price": price,
        "time": now_time()
    })
    save_data(data)


def cart_purchase(data: Dict[str, Any], remaining: float) -> None:
    print(f"\n{Colors.CYAN}{Colors.BOLD}📦 CART PURCHASE MODE{Colors.RESET}")
    divider()

    cart_items = []
    cart_total = 0.0

    while True:
        item_name = input("Item name (or 'done'): ").strip()

        if item_name.lower() == "done":
            break

        if not item_name:
            print(f"{Colors.RED}❌ Empty name not allowed.{Colors.RESET}")
            continue

        category = safe_non_empty("Category: ")
        price = safe_float_input("Price: $")

        if price <= 0:
            print(f"{Colors.RED}❌ Price must be greater than 0.{Colors.RESET}")
            continue

        cart_items.append((item_name, category, price))
        cart_total += price

        print(f"{Colors.GREEN}✅ Added: {item_name} (${price:.2f}){Colors.RESET}")

    if not cart_items:
        print(f"{Colors.YELLOW}❌ No items added to cart.{Colors.RESET}")
        return

    divider()
    print(f"{Colors.BOLD}🧾 Cart Total: ${cart_total:.2f}{Colors.RESET}")
    divider()

    if cart_total > remaining:
        print(f"{Colors.RED}❌ Can't afford cart. Need ${cart_total - remaining:.2f} more.{Colors.RESET}")
        return

    confirm = input("Confirm cart purchase? (yes/no): ").lower().strip()
    if confirm != "yes":
        print(f"{Colors.YELLOW}❌ Cart cancelled.{Colors.RESET}")
        return

    for name, cat, price in cart_items:
        add_purchase(data, name, cat, price)

    print(f"{Colors.GREEN}✅ Cart purchased successfully!{Colors.RESET}")


def delete_purchase(data: Dict[str, Any]) -> None:
    if not data["purchases"]:
        print(f"{Colors.YELLOW}📭 No purchases to delete.{Colors.RESET}")
        return

    show_history(data)
    index = safe_int_input("\nEnter purchase number to delete: ")

    if index < 1 or index > len(data["purchases"]):
        print(f"{Colors.RED}❌ Invalid purchase number.{Colors.RESET}")
        return

    removed = data["purchases"].pop(index - 1)
    data["last_deleted"] = removed
    save_data(data)

    print(f"{Colors.GREEN}✅ Deleted: {removed['name']} (${removed['price']:.2f}){Colors.RESET}")
    print(f"{Colors.YELLOW}💡 Tip: Use UNDO option to restore last deleted item.{Colors.RESET}")


def undo_delete(data: Dict[str, Any]) -> None:
    if data.get("last_deleted") is None:
        print(f"{Colors.RED}❌ Nothing to undo.{Colors.RESET}")
        return

    restored = data["last_deleted"]
    data["purchases"].append(restored)
    data["last_deleted"] = None

    save_data(data)
    print(f"{Colors.GREEN}✅ Undo successful! Restored: {restored['name']} (${restored['price']:.2f}){Colors.RESET}")


def edit_purchase(data: Dict[str, Any]) -> None:
    if not data["purchases"]:
        print(f"{Colors.YELLOW}📭 No purchases to edit.{Colors.RESET}")
        return

    show_history(data)
    index = safe_int_input("\nEnter purchase number to edit: ")

    if index < 1 or index > len(data["purchases"]):
        print(f"{Colors.RED}❌ Invalid purchase number.{Colors.RESET}")
        return

    item = data["purchases"][index - 1]

    print(f"\n{Colors.CYAN}{Colors.BOLD}✏ EDIT PURCHASE MODE{Colors.RESET}")
    divider()
    print(f"Name     : {item['name']}")
    print(f"Category : {item['category']}")
    print(f"Price    : ${item['price']:.2f}")
    print(f"Time     : {item['time']}")
    divider()

    new_name = input("New name (Enter to keep same): ").strip()
    new_category = input("New category (Enter to keep same): ").strip()
    new_price_input = input("New price (Enter to keep same): ").strip()

    if new_name:
        item["name"] = new_name

    if new_category:
        item["category"] = new_category.title()

    if new_price_input:
        try:
            new_price = float(new_price_input)
            if new_price <= 0:
                print(f"{Colors.RED}❌ Price must be > 0.{Colors.RESET}")
                return
            item["price"] = new_price
        except ValueError:
            print(f"{Colors.RED}❌ Invalid price input.{Colors.RESET}")
            return

    save_data(data)
    print(f"{Colors.GREEN}✅ Purchase updated successfully!{Colors.RESET}")


def search_purchase(data: Dict[str, Any]) -> None:
    if not data["purchases"]:
        print(f"{Colors.YELLOW}📭 No purchases available.{Colors.RESET}")
        return

    keyword = safe_non_empty("\nEnter keyword (name/category/id): ").lower()

    print(f"\n{Colors.CYAN}{Colors.BOLD}🔍 SEARCH RESULTS{Colors.RESET}")
    divider()

    found = False
    for item in data["purchases"]:
        if (keyword in item["name"].lower()
                or keyword in item["category"].lower()
                or keyword in item["id"].lower()):
            print(f"{Colors.BOLD}{item['name']}{Colors.RESET} | {item['category']} | ${item['price']:.2f}")
            print(f"ID: {item['id']} | 🕒 {item['time']}")
            divider()
            found = True

    if not found:
        print(f"{Colors.RED}❌ No matching results found.{Colors.RESET}")


def sort_purchases(data: Dict[str, Any]) -> None:
    if not data["purchases"]:
        print(f"{Colors.YELLOW}📭 No purchases to sort.{Colors.RESET}")
        return

    print(f"\n{Colors.CYAN}{Colors.BOLD}🔃 SORT OPTIONS{Colors.RESET}")
    divider()
    print("1. Price (High to Low)")
    print("2. Price (Low to High)")
    print("3. Date (Newest First)")
    print("4. Date (Oldest First)")
    print("5. Category (A-Z)")
    divider()

    choice = input("Choose (1-5): ").strip()

    if choice == "1":
        data["purchases"].sort(key=lambda x: x["price"], reverse=True)
    elif choice == "2":
        data["purchases"].sort(key=lambda x: x["price"])
    elif choice == "3":
        data["purchases"].sort(key=lambda x: parse_time(x["time"]), reverse=True)
    elif choice == "4":
        data["purchases"].sort(key=lambda x: parse_time(x["time"]))
    elif choice == "5":
        data["purchases"].sort(key=lambda x: x["category"])
    else:
        print(f"{Colors.RED}❌ Invalid sort option.{Colors.RESET}")
        return

    save_data(data)
    print(f"{Colors.GREEN}✅ Purchases sorted successfully!{Colors.RESET}")


# ================== DISCOUNT ==================
def discount_calculator() -> None:
    print(f"\n{Colors.CYAN}{Colors.BOLD}💸 DISCOUNT CALCULATOR{Colors.RESET}")
    divider()

    price = safe_float_input("Original price: $")
    discount = safe_int_input("Discount %: ")

    if discount < 0 or discount > 100:
        print(f"{Colors.RED}❌ Discount must be between 0 and 100.{Colors.RESET}")
        return

    discount_amount = price * (discount / 100)
    final_price = price - discount_amount

    divider()
    print(f"Original Price : ${price:.2f}")
    print(f"Discount       : {discount}% (-${discount_amount:.2f})")
    print(f"Final Price    : ${final_price:.2f}")
    divider()


# ================== REPORTS ==================
def category_summary(data: Dict[str, Any]) -> None:
    if not data["purchases"]:
        print(f"{Colors.YELLOW}📭 No purchases available.{Colors.RESET}")
        return

    summary = {}
    for item in data["purchases"]:
        summary[item["category"]] = summary.get(item["category"], 0) + item["price"]

    print(f"\n{Colors.CYAN}{Colors.BOLD}📊 CATEGORY SUMMARY REPORT{Colors.RESET}")
    divider()

    for cat, total in summary.items():
        print(f"{cat:<25} : ${total:.2f}")

    divider()


def spending_chart(data: Dict[str, Any]) -> None:
    if not data["purchases"]:
        print(f"{Colors.YELLOW}📭 No purchases available.{Colors.RESET}")
        return

    summary = {}
    for item in data["purchases"]:
        summary[item["category"]] = summary.get(item["category"], 0) + item["price"]

    max_spent = max(summary.values())

    print(f"\n{Colors.CYAN}{Colors.BOLD}📊 SPENDING BAR CHART{Colors.RESET}")
    divider()

    for cat, total in summary.items():
        bar_len = int((total / max_spent) * 55)
        bar = "█" * bar_len
        print(f"{cat:<20} | {bar:<55} ${total:.2f}")

    divider()


def daily_report(data: Dict[str, Any]) -> None:
    if not data["purchases"]:
        print(f"{Colors.YELLOW}📭 No purchases available.{Colors.RESET}")
        return

    report = {}
    for item in data["purchases"]:
        date = item["time"].split(" ")[0]
        report[date] = report.get(date, 0) + item["price"]

    print(f"\n{Colors.CYAN}{Colors.BOLD}📅 DAILY SPENDING REPORT{Colors.RESET}")
    divider()

    for date, total in report.items():
        print(f"{date:<15} : ${total:.2f}")

    divider()


def top_5_expensive(data: Dict[str, Any]) -> None:
    if not data["purchases"]:
        print(f"{Colors.YELLOW}📭 No purchases available.{Colors.RESET}")
        return

    sorted_items = sorted(data["purchases"], key=lambda x: x["price"], reverse=True)

    print(f"\n{Colors.CYAN}{Colors.BOLD}🔥 TOP 5 MOST EXPENSIVE PURCHASES{Colors.RESET}")
    divider()

    for i, item in enumerate(sorted_items[:5], start=1):
        print(f"{i}. {item['name']} | {item['category']} | ${item['price']:.2f}")

    divider()


def analytics_dashboard(data: Dict[str, Any]) -> None:
    if not data["purchases"]:
        print(f"{Colors.YELLOW}📭 No purchases available.{Colors.RESET}")
        return

    total_spent = data["spent"]
    budget = data["budget"]
    remaining = budget - total_spent
    total_items = len(data["purchases"])
    avg_spent = total_spent / total_items if total_items else 0

    summary = {}
    for item in data["purchases"]:
        summary[item["category"]] = summary.get(item["category"], 0) + item["price"]

    most_category = max(summary, key=summary.get)
    most_value = summary[most_category]

    cheapest = min(data["purchases"], key=lambda x: x["price"])
    expensive = max(data["purchases"], key=lambda x: x["price"])

    print(f"\n{Colors.CYAN}{Colors.BOLD}📈 ANALYTICS DASHBOARD (COMPANY REPORT){Colors.RESET}")
    divider()
    print(f"Total Purchases        : {total_items}")
    print(f"Total Spent            : ${total_spent:.2f}")
    print(f"Remaining Budget       : ${remaining:.2f}")
    print(f"Average Purchase Cost  : ${avg_spent:.2f}")
    divider()
    print(f"🔥 Highest Spending Category : {most_category} (${most_value:.2f})")
    print(f"💎 Cheapest Purchase         : {cheapest['name']} (${cheapest['price']:.2f})")
    print(f"💸 Most Expensive Purchase   : {expensive['name']} (${expensive['price']:.2f})")
    divider()

    if avg_spent > 0:
        prediction = int(remaining / avg_spent)
        print(f"📌 Prediction: You can buy approx {prediction} more items.")
    else:
        print("📌 Prediction: Not enough data for prediction.")

    divider()


# ================== EXPORT ==================
def export_to_csv(data: Dict[str, Any]) -> None:
    if not data["purchases"]:
        print(f"{Colors.YELLOW}📭 No purchases to export.{Colors.RESET}")
        return

    with open(EXPORT_CSV, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["No", "Purchase ID", "Item Name", "Category", "Price", "Time"])

        for i, item in enumerate(data["purchases"], start=1):
            writer.writerow([i, item["id"], item["name"], item["category"], item["price"], item["time"]])

    print(f"{Colors.GREEN}✅ Exported successfully to CSV: {EXPORT_CSV}{Colors.RESET}")


def export_to_json(data: Dict[str, Any]) -> None:
    if not data["purchases"]:
        print(f"{Colors.YELLOW}📭 No purchases to export.{Colors.RESET}")
        return

    with open(EXPORT_JSON, "w") as file:
        json.dump(data["purchases"], file, indent=4)

    print(f"{Colors.GREEN}✅ Exported successfully to JSON: {EXPORT_JSON}{Colors.RESET}")


# ================== RESET SYSTEM ==================
def reset_week(data: Dict[str, Any]) -> Dict[str, Any]:
    confirm = input("Reset purchases and start new week? (yes/no): ").lower().strip()

    if confirm != "yes":
        print(f"{Colors.YELLOW}❌ Reset cancelled.{Colors.RESET}")
        return data

    new_budget = safe_float_input("Enter new weekly budget: $")

    if new_budget <= 0:
        print(f"{Colors.RED}❌ Budget must be greater than 0.{Colors.RESET}")
        return data

    data = {"budget": new_budget, "spent": 0.0, "purchases": [], "last_deleted": None}
    save_data(data)

    print(f"{Colors.GREEN}✅ New week started successfully!{Colors.RESET}")
    return data


# ================== MAIN PROGRAM ==================
def main() -> None:
    show_welcome()
    data = load_data()

    if data["budget"] <= 0:
        print(f"{Colors.YELLOW}⚡ First time setup{Colors.RESET}")
        budget = safe_float_input("Enter your weekly budget: $")

        if budget <= 0:
            print(f"{Colors.RED}❌ Budget must be greater than 0.{Colors.RESET}")
            return

        data["budget"] = budget
        save_data(data)

    while True:
        remaining = budget_status(data)

        print(f"\n{Colors.BOLD}📌 MAIN MENU{Colors.RESET}")
        divider()
        print("1. Add purchase")
        print("2. Cart purchases")
        print("3. Discount calculator")
        print("4. View history")
        print("5. Search purchase")
        print("6. Edit purchase")
        print("7. Delete purchase")
        print("8. Undo delete ⭐")
        print("9. Sort purchases")
        print("10. Category summary")
        print("11. Spending chart")
        print("12. Daily report")
        print("13. Top 5 expensive purchases")
        print("14. Analytics dashboard ⭐")
        print("15. Export CSV")
        print("16. Export JSON")
        print("17. Backup data")
        print("18. Reset week")
        print("19. Exit")
        divider()

        choice = input("Choose option (1-19): ").strip()

        if choice == "1":
            name = safe_non_empty("Item name: ")
            category = safe_non_empty("Category: ")
            price = safe_float_input("Item price: $")

            if can_buy(price, remaining):
                add_purchase(data, name, category, price)
                print(f"{Colors.GREEN}✅ Purchase saved successfully!{Colors.RESET}")
            else:
                print(f"{Colors.RED}❌ Not affordable. Need ${price - remaining:.2f} more.{Colors.RESET}")

        elif choice == "2":
            cart_purchase(data, remaining)

        elif choice == "3":
            discount_calculator()

        elif choice == "4":
            show_history(data)

        elif choice == "5":
            search_purchase(data)

        elif choice == "6":
            edit_purchase(data)

        elif choice == "7":
            delete_purchase(data)

        elif choice == "8":
            undo_delete(data)

        elif choice == "9":
            sort_purchases(data)

        elif choice == "10":
            category_summary(data)

        elif choice == "11":
            spending_chart(data)

        elif choice == "12":
            daily_report(data)

        elif choice == "13":
            top_5_expensive(data)

        elif choice == "14":
            analytics_dashboard(data)

        elif choice == "15":
            export_to_csv(data)

        elif choice == "16":
            export_to_json(data)

        elif choice == "17":
            backup_data()

        elif choice == "18":
            data = reset_week(data)

        elif choice == "19":
            print(f"\n{Colors.GREEN}👋 Exiting Budget Tracker...{Colors.RESET}")
            break

        else:
            print(f"{Colors.RED}❌ Invalid option. Choose between 1-19.{Colors.RESET}")

    divider()
    print(f"{Colors.CYAN}{Colors.BOLD}FINAL SUMMARY REPORT{Colors.RESET}")
    divider()
    print(f"Budget    : ${data['budget']:.2f}")
    print(f"Spent     : ${data['spent']:.2f}")
    print(f"Remaining : ${data['budget'] - data['spent']:.2f}")
    print(f"Purchases : {len(data['purchases'])}")
    divider()


if __name__ == "__main__":
    main()
