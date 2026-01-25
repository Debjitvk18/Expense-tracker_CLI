from expense_tracker.db.connection import get_connection
from rich.console import Console
from rich.table import Table

console = Console()


def show_category_breakdown(user):
    """
    Display detailed category-wise expense breakdown with percentages.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                category,
                COALESCE(SUM(amount), 0) AS total_spent,
                COUNT(*) AS transaction_count,
                COALESCE(AVG(amount), 0) AS avg_amount
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

        # Calculate total for percentage
        total_expenses = sum(row[1] for row in rows)

        table = Table(title="📂 Detailed Category-wise Breakdown")

        table.add_column("Category", style="cyan")
        table.add_column("Total Spent", style="yellow", justify="right")
        table.add_column("% of Total", style="magenta", justify="right")
        table.add_column("Transactions", style="green", justify="right")
        table.add_column("Avg/Transaction", style="blue", justify="right")

        for category, total, count, avg in rows:
            percentage = (total / total_expenses * 100) if total_expenses > 0 else 0
            table.add_row(
                category,
                f"₹{total:,.2f}",
                f"{percentage:.1f}%",
                str(count),
                f"₹{avg:,.2f}"
            )

        # Add total row
        table.add_row(
            "TOTAL",
            f"₹{total_expenses:,.2f}",
            "100.0%",
            str(sum(row[2] for row in rows)),
            "",
            style="bold"
        )

        console.print(table)

    except Exception as e:
        print("❌ Failed to generate category breakdown:", e)

