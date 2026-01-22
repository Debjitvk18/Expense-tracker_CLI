from expense_tracker.db.connection import get_connection
from rich.console import Console
from rich.table import Table

console = Console()


def show_category_analysis(user):
    """
    Display category-wise expense totals for the user.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                category,
                COALESCE(SUM(amount), 0) AS total_spent
            FROM expenses
            WHERE user_id = %s
              AND type = 'expense'
            GROUP BY category
            ORDER BY total_spent DESC;
            """,
            (user["user_id"],)
        )

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            print("ℹ️ No expense data available for analysis.")
            return

        table = Table(title="📂 Category-wise Spending")

        table.add_column("Category", style="cyan")
        table.add_column("Total Spent", style="yellow")

        for category, total in rows:
            table.add_row(category, f"{total}")

        console.print(table)

    except Exception as e:
        print("❌ Failed to generate category analysis:", e)
