"""
SIMPLE BUDGET TRACKER
=====================
A beginner-friendly program to track your spending

Concepts covered:
✓ Variables & Data Types (int, float, string, bool)
✓ Basic Math Operations
✓ Print & Input Functions
✓ If-Else Conditionals
✓ Boolean Logic & Logical Operators (and, or, not)
✓ For Loops & While Loops
✓ Break & Continue
✓ Functions with Parameters & Return Values
✓ Code Modularity
"""


# ========== FUNCTIONS ==========

def show_welcome():
    """Display welcome message"""
    print("\n💰 WELCOME TO BUDGET TRACKER 💰")
    print("-" * 40)


def get_budget_status(budget, spent):
    """
    Calculate and show budget information
    Parameters: budget (float), spent (float)
    Returns: remaining budget (float)
    """
    remaining = budget - spent
    percentage = (spent / budget) * 100

    print(f"\nBudget: ${budget:.2f}")
    print(f"Spent: ${spent:.2f}")
    print(f"Remaining: ${remaining:.2f} ({100 - percentage:.1f}% left)")

    # Conditional to give advice
    if remaining > budget * 0.5:
        print("✓ Status: Good!")
    elif remaining > 0:
        print("⚠ Status: Be careful!")
    else:
        print("❌ Status: Over budget!")

    return remaining


def can_buy(item_price, remaining):
    """
    Check if item is affordable
    Parameters: item_price (float), remaining (float)
    Returns: True or False (bool)
    """
    # Using logical operator AND
    if item_price > 0 and item_price <= remaining:
        return True
    else:
        return False


def calculate_discount(price, discount_percent):
    """
    Calculate price after discount
    Parameters: price (float), discount_percent (int)
    Returns: discounted price (float)
    """
    discount = price * (discount_percent / 100)
    final_price = price - discount

    print(f"Original: ${price:.2f}")
    print(f"Discount: {discount_percent}% off (${discount:.2f})")
    print(f"Final: ${final_price:.2f}")

    return final_price


# ========== MAIN PROGRAM ==========

def main():
    """Main function - runs the entire program"""

    # Show welcome
    show_welcome()

    # VARIABLES - Different data types
    budget = float(input("\nEnter your weekly budget: $"))
    total_spent = 0.0
    purchase_count = 0

    # Boolean variable to control loop
    keep_going = True

    # WHILE LOOP - Main program loop
    while keep_going:

        # Show current status
        remaining = get_budget_status(budget, total_spent)

        print("\n" + "=" * 40)
        print("MENU:")
        print("1. Add a purchase")
        print("2. Buy multiple items")
        print("3. Calculate discount")
        print("4. Exit")
        print("=" * 40)

        choice = input("Choose (1-4): ")

        # ===== OPTION 1: Single Purchase =====
        if choice == '1':
            print("\n--- Add Purchase ---")
            item_name = input("Item name: ")
            item_price = float(input("Item price: $"))

            # Check if affordable using function
            if can_buy(item_price, remaining):
                confirm = input(f"Buy {item_name} for ${item_price:.2f}? (yes/no): ")

                if confirm.lower() == 'yes':
                    total_spent += item_price
                    purchase_count += 1
                    print(f"✓ Purchased {item_name}!")
                else:
                    print("Purchase cancelled.")
            else:
                shortage = item_price - remaining
                print(f"❌ Can't afford! Need ${shortage:.2f} more.")

        # ===== OPTION 2: Multiple Items =====
        elif choice == '2':
            print("\n--- Multiple Items ---")
            print("Enter items (type 'done' to finish)")

            item_count = 0
            cart_total = 0.0

            # WHILE LOOP with BREAK and CONTINUE
            while True:
                item = input(f"\nItem #{item_count + 1} name (or 'done'): ")

                # BREAK - Exit loop
                if item.lower() == 'done':
                    break

                # CONTINUE - Skip if empty
                if item.strip() == "":
                    print("Empty name! Try again.")
                    continue

                price = float(input(f"Price for {item}: $"))

                # CONTINUE - Skip if invalid price
                if price <= 0:
                    print("Invalid price! Try again.")
                    continue

                cart_total += price
                item_count += 1
                print(f"✓ Added {item}")

            # Check if any items added
            if item_count == 0:
                print("No items added.")
            else:
                print(f"\n📦 Cart: {item_count} items, Total: ${cart_total:.2f}")

                # Boolean logic: AND and OR operators
                affordable = cart_total <= remaining
                reasonable = cart_total <= remaining * 0.7

                if affordable and reasonable:
                    print("✓ Safe to buy!")
                elif affordable and not reasonable:
                    print("⚠ You can afford it, but it's tight.")
                else:
                    print("❌ Can't afford this cart.")

                # Ask to confirm
                if affordable:
                    confirm = input("Proceed with purchase? (yes/no): ")
                    if confirm.lower() == 'yes':
                        total_spent += cart_total
                        purchase_count += item_count
                        print("✓ Purchase complete!")

        # ===== OPTION 3: Discount Calculator =====
        elif choice == '3':
            print("\n--- Discount Calculator ---")
            original = float(input("Original price: $"))
            discount = int(input("Discount %: "))

            # Validate discount
            if discount < 0 or discount > 100:
                print("Invalid discount!")
                continue

            final = calculate_discount(original, discount)

            # Check affordability
            if can_buy(final, remaining):
                print("✓ You can afford this!")
            else:
                print("❌ Still too expensive.")

        # ===== OPTION 4: Exit =====
        elif choice == '4':
            keep_going = False  # This stops the while loop
            print("\nExiting...")

        # ===== Invalid Option =====
        else:
            print("❌ Invalid choice!")

    # ========== FINAL SUMMARY ==========
    print("\n" + "=" * 40)
    print("FINAL SUMMARY")
    print("=" * 40)
    print(f"Budget: ${budget:.2f}")
    print(f"Spent: ${total_spent:.2f}")
    print(f"Remaining: ${budget - total_spent:.2f}")
    print(f"Total Purchases: {purchase_count}")

    # FOR LOOP - Show shopping behavior
    print("\n📊 Shopping Behavior:")
    levels = ["Saver 💎", "Moderate 👍", "Spender 💸"]

    spent_percentage = (total_spent / budget) * 100

    # Determine behavior level
    if spent_percentage < 50:
        level_index = 0
    elif spent_percentage < 80:
        level_index = 1
    else:
        level_index = 2

    # FOR LOOP - Display with stars
    for i in range(len(levels)):
        if i == level_index:
            print(f"  → {levels[i]} ⭐ (You are here!)")
        else:
            print(f"    {levels[i]}")

    print("\n" + "=" * 40)
    print("Thanks for using Budget Tracker! 👋")


# ========== START PROGRAM ==========
if __name__ == "__main__":
    main()
