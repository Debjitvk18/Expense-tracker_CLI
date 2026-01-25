from expense_tracker.db.connection import get_connection
from expense_tracker.expenses.filters import (
    filter_by_date_range,
    filter_by_category,
    filter_by_amount_range
)
from rich.console import Console
from rich.table import Table
from datetime import datetime

console = Console()


def display_expense_table(rows, title="Expense History"):
    """
    Helper function to display expenses in a table format.
    """
    if not rows:
        print("ℹ️ No expenses found.")
        return

    table = Table(title=title)

    table.add_column("Date", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("Amount", style="yellow", justify="right")
    table.add_column("Payment")
    table.add_column("Receiver")
    table.add_column("Description")

    for row in rows:
        expense_date, type_, category, amount, payment, receiver, description = row

        # Color code based on type
        type_style = "green" if type_ == "income" else "red"
        amount_formatted = f"₹{amount:,.2f}"

        table.add_row(
            str(expense_date),
            type_,
            category,
            amount_formatted,
            payment or "-",
            receiver or "-",
            description or "-",
            style=type_style if type_ == "income" else ""
        )

    console.print(table)

    # Display summary
    total = sum(row[3] for row in rows)
    print(f"\n📊 Total shown: ₹{total:,.2f} | Transactions: {len(rows)}")


def view_all_expenses(user):
    """
    View all expenses without filters.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                expense_date,
                type,
                category,
                amount,
                payment_method,
                receiver,
                description
            FROM expenses
            WHERE user_id = %s
            ORDER BY expense_date DESC;
            """,
            (user["user_id"],)
        )

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        display_expense_table(rows, "📄 All Expenses")

    except Exception as e:
        print("❌ Failed to fetch expenses:", e)


def view_filtered_by_date(user):
    """
    View expenses filtered by date range.
    """
    try:
        print("\n📅 Filter by Date Range")
        start_date = input("Start date (YYYY-MM-DD): ").strip()
        end_date = input("End date (YYYY-MM-DD): ").strip()

        # Validate dates
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
            return

        rows = filter_by_date_range(user["user_id"], start_date, end_date)
        display_expense_table(rows, f"📄 Expenses from {start_date} to {end_date}")

    except Exception as e:
        print("❌ Failed to filter by date:", e)


def view_filtered_by_category(user):
    """
    View expenses filtered by category.
    """
    try:
        # First, show available categories
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT DISTINCT category
            FROM expenses
            WHERE user_id = %s
            ORDER BY category;
            """,
            (user["user_id"],)
        )

        categories = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        if not categories:
            print("ℹ️ No categories found.")
            return

        print("\n📂 Available Categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")

        print(f"{len(categories) + 1}. Enter custom category")

        choice = input("\nChoose a category number: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = categories[int(choice) - 1]
        elif choice.isdigit() and int(choice) == len(categories) + 1:
            category = input("Enter category name: ").strip()
        else:
            print("❌ Invalid choice.")
            return

        rows = filter_by_category(user["user_id"], category)
        display_expense_table(rows, f"📄 Expenses in category: {category}")

    except Exception as e:
        print("❌ Failed to filter by category:", e)


def view_filtered_by_amount(user):
    """
    View expenses filtered by amount range.
    """
    try:
        print("\n💰 Filter by Amount Range")
        min_amount = float(input("Minimum amount: ").strip())
        max_amount = float(input("Maximum amount: ").strip())

        if min_amount < 0 or max_amount < 0 or min_amount > max_amount:
            print("❌ Invalid amount range.")
            return

        rows = filter_by_amount_range(user["user_id"], min_amount, max_amount)
        display_expense_table(rows, f"📄 Expenses between ₹{min_amount:,.2f} and ₹{max_amount:,.2f}")

    except ValueError:
        print("❌ Please enter valid numbers.")
    except Exception as e:
        print("❌ Failed to filter by amount:", e)


def view_expenses(user):
    """
    Main view expenses menu with filtering options.
    """
    while True:
        print("\n📄 VIEW EXPENSES")
        print("=" * 40)
        print("1. 📋 View All Expenses")
        print("2. 📅 Filter by Date Range")
        print("3. 📂 Filter by Category")
        print("4. 💰 Filter by Amount Range")
        print("5. 🔙 Back to Dashboard")
        print("=" * 40)

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_all_expenses(user)
        elif choice == "2":
            view_filtered_by_date(user)
        elif choice == "3":
            view_filtered_by_category(user)
        elif choice == "4":
            view_filtered_by_amount(user)
        elif choice == "5":
            print("🔙 Returning to Dashboard...")
            break
        else:
            print("❌ Invalid choice. Please try again.")

