from expense_tracker.db.connection import get_connection
from rich.console import Console
from rich.table import Table

console = Console()


def show_summary(user):
    """
    Show total income, total expense, and savings for the user.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Total income
        cursor.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE user_id = %s AND type = 'income';
            """,
            (user["user_id"],)
        )
        total_income = cursor.fetchone()[0]

        # Total expense
        cursor.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE user_id = %s AND type = 'expense';
            """,
            (user["user_id"],)
        )
        total_expense = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        savings = total_income - total_expense

        # Display summary table
        table = Table(title="💰 Financial Summary")

        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Amount", style="green")

        table.add_row("Total Income", f"{total_income}")
        table.add_row("Total Expense", f"{total_expense}")
        table.add_row("Savings", f"{savings}")

        console.print(table)

    except Exception as e:
        print("❌ Failed to generate summary:", e)
