import json
import datetime
from collections import defaultdict

class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = self.load_expenses()
    
    def load_expenses(self):
        """Load expenses from file."""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_expenses(self):
        """Save expenses to file."""
        with open(self.filename, 'w') as f:
            json.dump(self.expenses, f, indent=2)
    
    def add_expense(self, amount, category, description=""):
        """Add a new expense."""
        expense = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "amount": float(amount),
            "category": category,
            "description": description
        }
        self.expenses.append(expense)
        self.save_expenses()
        print(f"Added expense: ${amount} for {category}")
    
    def view_expenses(self):
        """Display all expenses."""
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        
        print("\n=== All Expenses ===")
        total = 0
        for expense in self.expenses:
            print(f"{expense['date']} | ${expense['amount']:.2f} | {expense['category']} | {expense['description']}")
            total += expense['amount']
        print(f"\nTotal spent: ${total:.2f}")
    
    def view_by_category(self):
        """Display expenses grouped by category."""
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        
        categories = defaultdict(float)
        for expense in self.expenses:
            categories[expense['category']] += expense['amount']
        
        print("\n=== Expenses by Category ===")
        for category, amount in sorted(categories.items()):
            print(f"{category}: ${amount:.2f}")

def main():
    tracker = ExpenseTracker()
    
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. View by category")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ")
        
        if choice == "1":
            try:
                amount = float(input("Enter amount: $"))
                category = input("Enter category (food, transport, entertainment, etc.): ")
                description = input("Enter description (optional): ")
                tracker.add_expense(amount, category, description)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        elif choice == "2":
            tracker.view_expenses()
        
        elif choice == "3":
            tracker.view_by_category()
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
