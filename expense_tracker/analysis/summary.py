from expense_tracker.db.connection import get_connection
from expense_tracker.analysis.charts import (
    daily_expense_line_chart,
    monthly_expense_line_chart,
    category_spending_bar_chart,
    category_spending_pie_chart,
    payment_method_pie_chart,
    income_vs_expense_comparison
)
from expense_tracker.analysis.category_analysis import show_category_breakdown
from rich.console import Console
from rich.table import Table

console = Console()


def show_financial_summary(user):
    """
    Show detailed financial summary with all metrics.
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

        # Count of transactions
        cursor.execute(
            """
            SELECT 
                COUNT(CASE WHEN type = 'income' THEN 1 END) as income_count,
                COUNT(CASE WHEN type = 'expense' THEN 1 END) as expense_count,
                COUNT(*) as total_count
            FROM expenses
            WHERE user_id = %s;
            """,
            (user["user_id"],)
        )
        income_count, expense_count, total_count = cursor.fetchone()

        # Average expense
        cursor.execute(
            """
            SELECT COALESCE(AVG(amount), 0)
            FROM expenses
            WHERE user_id = %s AND type = 'expense';
            """,
            (user["user_id"],)
        )
        avg_expense = cursor.fetchone()[0]

        # Highest expense
        cursor.execute(
            """
            SELECT COALESCE(MAX(amount), 0), category
            FROM expenses
            WHERE user_id = %s AND type = 'expense'
            GROUP BY category
            ORDER BY MAX(amount) DESC
            LIMIT 1;
            """,
            (user["user_id"],)
        )
        highest_result = cursor.fetchone()
        highest_expense = highest_result[0] if highest_result else 0
        highest_category = highest_result[1] if highest_result else "N/A"

        cursor.close()
        conn.close()

        savings = total_income - total_expense
        savings_rate = (savings / total_income * 100) if total_income > 0 else 0

        # Display comprehensive summary table
        table = Table(title="💰 Comprehensive Financial Summary", show_header=True)

        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        table.add_row("Total Income", f"₹{total_income:,.2f}")
        table.add_row("Total Expenses", f"₹{total_expense:,.2f}")
        table.add_row("Net Savings", f"₹{savings:,.2f}", style="bold green" if savings >= 0 else "bold red")
        table.add_row("Savings Rate", f"{savings_rate:.1f}%")
        table.add_row("", "")  # Separator
        table.add_row("Income Transactions", f"{income_count}")
        table.add_row("Expense Transactions", f"{expense_count}")
        table.add_row("Total Transactions", f"{total_count}")
        table.add_row("", "")  # Separator
        table.add_row("Average Expense", f"₹{avg_expense:,.2f}")
        table.add_row("Highest Expense", f"₹{highest_expense:,.2f}")
        table.add_row("Highest Spending Category", highest_category)

        console.print(table)

    except Exception as e:
        print("❌ Failed to generate summary:", e)


def show_summary(user):
    """
    Main analysis menu with all visualization and analysis options.
    """
    while True:
        print("\n📊 ANALYSIS & REPORTS")
        print("=" * 40)
        print("1. 💰 Financial Summary")
        print("2. 📈 Daily Expense Trend (Line Chart)")
        print("3. 📈 Monthly Expense Trend (Line Chart)")
        print("4. 📊 Category Spending (Bar Chart)")
        print("5. 🥧 Category Distribution (Pie Chart)")
        print("6. 🥧 Payment Method Distribution (Pie Chart)")
        print("7. 📊 Income vs Expense Comparison")
        print("8. 📋 Detailed Category Breakdown")
        print("9. 🔙 Back to Dashboard")
        print("=" * 40)

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_financial_summary(user)
        elif choice == "2":
            daily_expense_line_chart(user)
        elif choice == "3":
            monthly_expense_line_chart(user)
        elif choice == "4":
            category_spending_bar_chart(user)
        elif choice == "5":
            category_spending_pie_chart(user)
        elif choice == "6":
            payment_method_pie_chart(user)
        elif choice == "7":
            income_vs_expense_comparison(user)
        elif choice == "8":
            show_category_breakdown(user)
        elif choice == "9":
            print("🔙 Returning to Dashboard...")
            break
        else:
            print("❌ Invalid choice. Please try again.")
