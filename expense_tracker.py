import csv
import os
from datetime import datetime

FILE = "expenses.csv"

def init_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Description", "Amount"])  # header

# Add a new expense
def add_expense():
    date = input("Enter date (DD-MM-YYYY): ")
    desc = input("Enter description: ")
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount! Please enter a number.")
        return

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, desc, amount])
    print("Expense added successfully!")

def view_expense():
    if not os.path.exists(FILE):
        print("No expenses found.")
        return
    with open(FILE, "r") as f:
        reader = list(csv.reader(f))
        for i, row in enumerate(reader):
            print(f"{i}. {row}")

def total_expenses():
    if not os.path.exists(FILE):
        print("No expenses found.")
        return
    total = 0
    with open(FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            try:
                total += float(row[2])
            except:
                pass
    print("Total spent so far:", total)

def total_between_dates():
    if not os.path.exists(FILE):
        print("No expenses to calculate.")
        return

    start_date = input("Enter start date (DD-MM-YYYY): ")
    end_date = input("Enter end date (DD-MM-YYYY): ")

    try:
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
    except ValueError:
        print(" Invalid date format! Use DD-MM-YYYY.")
        return

    total = 0
    with open(FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            try:
                expense_date = datetime.strptime(row[0], "%d-%m-%Y")
                if start <= expense_date <= end:
                    total += float(row[2])
            except:
                pass
    print(f"Total spent from {start_date} to {end_date}: {total}")

def delete_expense():
    if not os.path.exists(FILE):
        print("No expenses to delete.")
        return
    with open(FILE, "r") as f:
        reader = list(csv.reader(f))

    if len(reader) <= 1:
        print("No expenses found")
        return

    print("\n--- Expenses List ---")
    for i, row in enumerate(reader):
        print(f"{i}. {row}")

    try:
        idx = int(input("Enter the index number to delete: "))
        if idx == 0:
            print("Header row cannot be removed")
            return
        removed = reader.pop(idx)
        print(f"Deleted: {removed}")
    except (ValueError, IndexError):
        print("Invalid index number!")
        return

    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(reader)

def main():
    init_file()
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total (All)")
        print("4. Delete Expense")
        print("5. Total Between Dates")
        print("6. Exit")

        choice = input("Choose option: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expense()  # fixed name
        elif choice == "3":
            total_expenses()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            total_between_dates()
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, try again!")

if __name__ == "__main__":
    main()
