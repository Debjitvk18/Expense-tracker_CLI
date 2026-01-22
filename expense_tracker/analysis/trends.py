from expense_tracker.db.connection import get_connection
from rich.console import Console
from rich.table import Table

console = Console()


def show_daily_trend(user):
    """
    Show daily expense trend for the user.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                expense_date,
                COALESCE(SUM(amount), 0) AS total_spent
            FROM expenses
            WHERE user_id = %s
              AND type = 'expense'
            GROUP BY expense_date
            ORDER BY expense_date;
            """,
            (user["user_id"],)
        )

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            print("ℹ️ No daily expense data available.")
            return

        table = Table(title="📅 Daily Expense Trend")
        table.add_column("Date", style="cyan")
        table.add_column("Total Spent", style="yellow")

        for expense_date, total in rows:
            table.add_row(str(expense_date), f"{total}")

        console.print(table)

    except Exception as e:
        print("❌ Failed to generate daily trend:", e)


def show_monthly_trend(user):
    """
    Show monthly expense trend for the user.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                TO_CHAR(expense_date, 'YYYY-MM') AS month,
                COALESCE(SUM(amount), 0) AS total_spent
            FROM expenses
            WHERE user_id = %s
              AND type = 'expense'
            GROUP BY month
            ORDER BY month;
            """,
            (user["user_id"],)
        )

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            print("ℹ️ No monthly expense data available.")
            return

        table = Table(title="🗓️ Monthly Expense Trend")
        table.add_column("Month", style="cyan")
        table.add_column("Total Spent", style="yellow")

        for month, total in rows:
            table.add_row(month, f"{total}")

        console.print(table)

    except Exception as e:
        print("❌ Failed to generate monthly trend:", e)
