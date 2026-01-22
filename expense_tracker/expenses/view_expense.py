from expense_tracker.db.connection import get_connection
from rich.console import Console
from rich.table import Table

console = Console()


def view_expenses(user):
    print("\n📄 Your Expenses")
    print("-" * 30)

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

        if not rows:
            print("ℹ️ No expenses found.")
            return

        table = Table(title="Expense History")

        table.add_column("Date", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Category", style="green")
        table.add_column("Amount", style="yellow")
        table.add_column("Payment")
        table.add_column("Receiver")
        table.add_column("Description")

        for row in rows:
            expense_date, type_, category, amount, payment, receiver, description = row

            table.add_row(
                str(expense_date),
                type_,
                category,
                f"{amount}",
                payment or "-",
                receiver or "-",
                description or "-"
            )

        console.print(table)

    except Exception as e:
        print("❌ Failed to fetch expenses:", e)
