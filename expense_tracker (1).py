# Personal Expense Tracker
# Subject: Python (5.0CE202E02H)
# Made by: Varsha Baghel (25/SET/BCSE/517)

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # saves charts as image files
import matplotlib.pyplot as plt

plt.rcParams["font.size"] = 12
FILE_NAME = "expenses.csv"
CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Education", "Other"]


class ExpenseTracker:
    def __init__(self):
        # constructor: load old data if the file already exists
        if os.path.exists(FILE_NAME):
            self.data = pd.read_csv(FILE_NAME)
        else:
            self.data = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

    def add_expense(self, date, category, description, amount):
        row = {"Date": date, "Category": category,
               "Description": description, "Amount": amount}
        self.data.loc[len(self.data)] = row
        self.data.to_csv(FILE_NAME, index=False)
        print("Expense added successfully!")

    def view_all(self):
        if self.data.empty:
            print("No expenses recorded yet.")
        else:
            print(self.data.to_string(index=False))

    def total_spent(self):
        return self.data["Amount"].sum()

    def category_summary(self):
        return self.data.groupby("Category")["Amount"].sum().sort_values(ascending=False)

    def search_category(self, category):
        return self.data[self.data["Category"] == category]

    def show_charts(self):
        if self.data.empty:
            print("No expenses to show. Please add some first.")
            return
        summary = self.category_summary()
        plt.figure(figsize=(9, 4.5))
        plt.subplot(1, 2, 1)
        plt.pie(summary, labels=summary.index, autopct="%1.1f%%")
        plt.title("Spending by Category")
        plt.subplot(1, 2, 2)
        plt.bar(summary.index, summary.values, color="teal")
        plt.title("Category-wise Total (Rs.)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig("expense_charts.png")
        print("Charts saved as expense_charts.png")


def get_amount():
    while True:
        try:
            amount = float(input("Enter Amount (Rs.): "))
            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                return amount
        except ValueError:
            print("Invalid input! Please enter a number.")


def main():
    tracker = ExpenseTracker()
    while True:
        print("-" * 45)
        print("      PERSONAL EXPENSE TRACKER")
        print("-" * 45)
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Show Total Spending")
        print("4. Category-wise Summary")
        print("5. Search by Category")
        print("6. Show Charts")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            date = input("Enter Date (dd-mm-yyyy): ")
            print("Categories:", ", ".join(CATEGORIES))
            category = input("Enter Category: ").title()
            if category not in CATEGORIES:
                category = "Other"
            description = input("Enter Description: ")
            amount = get_amount()
            tracker.add_expense(date, category, description, amount)
        elif choice == "2":
            tracker.view_all()
        elif choice == "3":
            print("Total spent: Rs.", tracker.total_spent())
        elif choice == "4":
            if tracker.data.empty:
                print("No expenses recorded yet.")
            else:
                print(tracker.category_summary())
        elif choice == "5":
            result = tracker.search_category(input("Enter Category to search: ").title())
            print(result.to_string(index=False) if not result.empty else "No records found.")
        elif choice == "6":
            tracker.show_charts()
        elif choice == "7":
            print("Thank you for using the tracker!")
            break
        else:
            print("Invalid choice! Try again.")


main()
