from expense_tracker.expenses.add_expense import add_expense
from expense_tracker.expenses.view_expense import view_expenses
from expense_tracker.analysis.summary import show_summary
from expense_tracker.core.session import clear_session


def start_app(user):
    """
    Main application loop (Dashboard)
    """
    while True:
        print("\n📊 DASHBOARD")
        print("-" * 20)
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Analysis")
        print("4. Logout")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(user)

        elif choice == "2":
            view_expenses(user)

        elif choice == "3":
            show_summary(user)

        elif choice == "4":
            clear_session()
            print("🔒 Logged out successfully.")
            break

        elif choice == "5":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid option. Please try again.")
