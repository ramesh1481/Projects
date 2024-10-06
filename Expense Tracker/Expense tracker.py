import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

class ExpenseTracker:
    def __init__(self, db_name="expenses.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.salary = 0

    def delete_expense(self, expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        self.conn.commit()
        print(f"Expense with ID {expense_id} deleted successfully.")

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                amount REAL,
                category TEXT
            )
        ''')
        self.conn.commit()

    def add_expense(self, date, amount, category):
        self.cursor.execute("INSERT INTO expenses (date, amount, category) VALUES (?, ?, ?)", (date, amount, category))
        self.conn.commit()

    def set_salary(self, salary):
        self.salary = salary

    def total_expenses(self):
        self.cursor.execute("SELECT SUM(amount) FROM expenses")
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0

    def view_expenses(self):
        df = self.get_expenses_dataframe()
        if df.empty:
            print("No expenses recorded yet.")
        else:
            print(df)
            print(f"Total Expenses: ${self.total_expenses()}")

    def view_categories(self):
        df = self.get_expenses_dataframe()
        if df.empty:
            print("No categories recorded yet.")
        else:
            print("Categories:")
            print(df['category'].unique())

    def budget_status(self):
        total_exp = self.total_expenses()
        remaining_budget = self.salary - total_exp
        if remaining_budget < 0:
            print(f"Status: Poor in budget (Exceeded by: ${-remaining_budget})")
        else:
            print(f"Status: Healthy in budget (Remaining salary: ${remaining_budget})")

    def plot_expenses(self):
        df = self.get_expenses_dataframe()
        if df.empty:
            print("No expenses to plot.")
            return

        category_expenses = df.groupby('category')['amount'].sum()
        
        plt.figure(figsize=(10, 6))
        category_expenses.plot(kind='bar')
        plt.xlabel("Categories")
        plt.ylabel("Total Expenses")
        plt.title("Expense Distribution by Category")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig("expense_plot.png") 
        print("Expense plot saved to expense_plot.png")

    def get_expenses_dataframe(self):
        self.cursor.execute("SELECT * FROM expenses")
        rows = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return pd.DataFrame(rows, columns=columns)

    def close_connection(self):
        self.conn.close()

tracker = ExpenseTracker()

while True:
    print("\nExpense Tracker Menu:")
    print("1. Add Expense")
    print("2. Set Salary")
    print("3. View Expenses")
    print("4. View Categories")
    print("5. Budget Status")
    print("6. Plot Expenses")
    print("7. Delete Expense")  
    print("8. Exit") 

    choice = input("Enter your choice: ")

    if choice == "1":
        date = input("Enter date (YYYY-MM-DD): ")
        amount = float(input("Enter amount: $"))
        category = input("Enter category: ")
        tracker.add_expense(date, amount, category)
    elif choice == "2":
        salary = float(input("Enter your salary amount: $"))
        tracker.set_salary(salary)
    elif choice == "3":
        tracker.view_expenses()
    elif choice == "4":
        tracker.view_categories()
    elif choice == "5":
        tracker.budget_status()
    elif choice == "6":
        tracker.plot_expenses()
    elif choice == "7":
        expense_id = int(input("Enter the ID of the expense to delete: "))
        tracker.delete_expense(expense_id)
    elif choice == "8":
        print("Exiting Expense Tracker. Goodbye!")
        tracker.close_connection()
        break
    else:
        print("Invalid choice. Please try again.")

