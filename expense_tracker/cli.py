from expense_tracker.core.session import load_session
from expense_tracker.auth.signup import signup
from expense_tracker.auth.login import login
from expense_tracker.core.app import start_app


def main():
    print("\n💸 Expense Tracker CLI")
    print("=" * 25)

    # 🔐 Check if user session exists
    session = load_session()

    if session:
        print(f"👋 Welcome back, {session['username']}!")
        start_app(session)
        return

    # 🆕 No session → ask user
    while True:
        print("\nAre you a new or existing user?")
        print("1. New User (Sign Up)")
        print("2. Existing User (Login)")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            user = signup()
            if user:
                start_app(user)
                break

        elif choice == "2":
            user = login()
            if user:
                start_app(user)
                break

        elif choice == "3":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")
