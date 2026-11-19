import csv
import json
from datetime import datetime
from collections import defaultdict

EXPENSE_FILE = "expenses.csv"
BUDGET_FILE = "budgets.json"

CATEGORIES = [
    "Food", "Travel", "Shopping",
    "Education", "Bills", "Health", "Other"
]

def create_files():
    try:
        with open(EXPENSE_FILE, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Category", "Amount", "Description"])
    except FileExistsError:
        pass

    try:
        with open(BUDGET_FILE, "x") as file:
            json.dump({}, file)
    except FileExistsError:
        pass


def load_expenses():
    expenses = []
    try:
        with open(EXPENSE_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append(row)
    except FileNotFoundError:
        pass
    return expenses


def save_expenses(expenses):
    with open(EXPENSE_FILE, "w", newline="") as file:
        fields = ["ID", "Date", "Category", "Amount", "Description"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(expenses)

def add_expense():
    expenses = load_expenses()

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        date = input("Enter date (YYYY-MM-DD): ")
        datetime.strptime(date, "%Y-%m-%d")

        print("Categories:", ", ".join(CATEGORIES))
        category = input("Enter category: ").strip().title()

        if category not in CATEGORIES:
            print("Invalid category.")
            return

        description = input("Enter description: ")

        new_id = max([int(e["ID"]) for e in expenses], default=0) + 1

        expense = {
            "ID": str(new_id),
            "Date": date,
            "Category": category,
            "Amount": str(amount),
            "Description": description
        }

        expenses.append(expense)
        save_expenses(expenses)
        print("Expense added successfully!")

    except ValueError:
        print("Invalid amount or date.")


def view_expenses():
    expenses = load_expenses()

    if not expenses:
        print("No expenses found.")
        return

    for e in expenses:
        print(e)


def edit_expense():
    expenses = load_expenses()
    expense_id = input("Enter expense ID to edit: ")

    for e in expenses:
        if e["ID"] == expense_id:
            try:
                amount = float(input("Enter new amount: "))
                if amount <= 0:
                    print("Amount must be positive.")
                    return

                date = input("Enter new date (YYYY-MM-DD): ")
                datetime.strptime(date, "%Y-%m-%d")

                category = input("Enter new category: ").strip().title()
                if category not in CATEGORIES:
                    print("Invalid category.")
                    return

                description = input("Enter new description: ")

                e["Amount"] = str(amount)
                e["Date"] = date
                e["Category"] = category
                e["Description"] = description

                save_expenses(expenses)
                print("Expense updated!")
                return

            except ValueError:
                print("Invalid amount or date.")
                return

    print("Expense ID not found.")

def delete_expense():
    expenses = load_expenses()
    expense_id = input("Enter expense ID to delete: ")

    new_expenses = []
    found = False

    for e in expenses:
        if e["ID"] == expense_id:
            found = True
        else:
            new_expenses.append(e)

    if found:
        save_expenses(new_expenses)
        print("Expense deleted!")
    else:
        print("Expense ID not found.")

def set_budget():
    try:
        month = input("Enter month (YYYY-MM): ")
        datetime.strptime(month, "%Y-%m")

        amount = float(input("Enter monthly budget: "))

        if amount <= 0:
            print("Budget must be positive.")
            return

        try:
            with open(BUDGET_FILE, "r") as file:
                budgets = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            budgets = {}

        budgets[month] = amount

        with open(BUDGET_FILE, "w") as file:
            json.dump(budgets, file, indent=4)

        print("Monthly budget saved!")

    except ValueError:
        print("Invalid month or budget.")


# Spending summary
def spending_summary():
    expenses = load_expenses()

    daily = defaultdict(float)
    monthly = defaultdict(float)
    category = defaultdict(float)

    for e in expenses:
        date = datetime.strptime(e["Date"], "%Y-%m-%d")
        amount = float(e["Amount"])

        daily[e["Date"]] += amount
        monthly[date.strftime("%Y-%m")] += amount
        category[e["Category"]] += amount

    print("\n--- DAILY SPENDING ---")
    for key, value in daily.items():
        print(key, ":", value)

    print("\n--- MONTHLY SPENDING ---")
    for key, value in monthly.items():
        print(key, ":", value)

    print("\n--- CATEGORY-WISE SPENDING ---")
    for key, value in category.items():
        print(key, ":", value)

    month = input("\nEnter month to check budget (YYYY-MM): ")

    try:
        with open(BUDGET_FILE, "r") as file:
            budgets = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        budgets = {}

    if month in budgets:
        budget = float(budgets[month])
        spent = monthly[month]

        print("Monthly Budget:", budget)
        print("Total Spent:", spent)
        print("Remaining:", budget - spent)

        if spent > budget:
            print("Warning! You exceeded your budget.")
    else:
        print("No budget set for this month.")


# Search and filter
def search_expenses():
    expenses = load_expenses()

    keyword = input(
        "Enter category, date (YYYY-MM-DD), or description to search: "
    ).strip().lower()

    found = False

    for e in expenses:
        if (keyword in e["Category"].lower()
                or keyword in e["Date"].lower()
                or keyword in e["Description"].lower()):
            print(e)
            found = True

    if not found:
        print("No matching expenses found.")


# Main menu
def main():
    create_files()

    while True:
        print("\n===== PERSONAL EXPENSE & BUDGET TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Set Monthly Budget")
        print("6. Spending Summary")
        print("7. Search Expenses")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            edit_expense()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            set_budget()
        elif choice == "6":
            spending_summary()
        elif choice == "7":
            search_expenses()
        elif choice == "8":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()