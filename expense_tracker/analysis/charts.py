import plotext as plt
from expense_tracker.db.connection import get_connection


def daily_expense_line_chart(user):
    """
    Display daily expense trend as ASCII line chart.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT expense_date, SUM(amount)
        FROM expenses
        WHERE user_id = %s AND type = 'expense'
        GROUP BY expense_date
        ORDER BY expense_date;
        """,
        (user["user_id"],)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print("ℹ️ No data available for daily chart.")
        return

    dates = [str(row[0]) for row in rows]
    amounts = [float(row[1]) for row in rows]

    plt.clear_figure()
    plt.title("📈 Daily Expense Trend")
    plt.xlabel("Date")
    plt.ylabel("Amount Spent")
    plt.plot(dates, amounts, marker="dot")
    plt.show()


def monthly_expense_line_chart(user):
    """
    Display monthly expense trend as ASCII line chart.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT TO_CHAR(expense_date, 'YYYY-MM'), SUM(amount)
        FROM expenses
        WHERE user_id = %s AND type = 'expense'
        GROUP BY 1
        ORDER BY 1;
        """,
        (user["user_id"],)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print("ℹ️ No data available for monthly chart.")
        return

    months = [row[0] for row in rows]
    amounts = [float(row[1]) for row in rows]

    plt.clear_figure()
    plt.title("📈 Monthly Expense Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount Spent")
    plt.plot(months, amounts, marker="dot")
    plt.show()


def category_spending_bar_chart(user):
    """
    Display category-wise spending as ASCII bar chart.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id = %s AND type = 'expense'
        GROUP BY category
        ORDER BY SUM(amount) DESC;
        """,
        (user["user_id"],)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print("ℹ️ No data available for category chart.")
        return

    categories = [row[0] for row in rows]
    amounts = [float(row[1]) for row in rows]

    plt.clear_figure()
    plt.title("📊 Category-wise Spending")
    plt.xlabel("Amount")
    plt.ylabel("Category")
    plt.bar(categories, amounts)
    plt.show()
