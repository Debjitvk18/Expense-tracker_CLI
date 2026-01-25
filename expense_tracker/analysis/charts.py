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


def category_spending_pie_chart(user):
    """
    Display category-wise spending distribution as pie chart.
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
        print("ℹ️ No data available for pie chart.")
        return

    categories = [row[0] for row in rows]
    amounts = [float(row[1]) for row in rows]
    total = sum(amounts)

    # Calculate percentages
    percentages = [(amt / total) * 100 for amt in amounts]

    plt.clear_figure()
    plt.title("🥧 Category Distribution (Pie Chart)")
    
    # Create simple pie chart using bar chart
    plt.simple_bar(categories, amounts, width=0.3, title="Category Spending Distribution")
    
    # Display percentages in console
    print("\n📊 Category Distribution:")
    print("-" * 50)
    for cat, amt, pct in zip(categories, amounts, percentages):
        bar_length = int(pct / 2)  # Scale down for display
        bar = "█" * bar_length
        print(f"{cat:20s} {bar:25s} ₹{amt:>10.2f} ({pct:>5.1f}%)")
    print("-" * 50)
    print(f"{'TOTAL':20s} {' ':25s} ₹{total:>10.2f} (100.0%)")


def payment_method_pie_chart(user):
    """
    Display payment method distribution as pie chart.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            COALESCE(payment_method, 'Not Specified') as method, 
            SUM(amount)
        FROM expenses
        WHERE user_id = %s AND type = 'expense'
        GROUP BY method
        ORDER BY SUM(amount) DESC;
        """,
        (user["user_id"],)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print("ℹ️ No data available for payment method chart.")
        return

    methods = [row[0] for row in rows]
    amounts = [float(row[1]) for row in rows]
    total = sum(amounts)

    # Calculate percentages
    percentages = [(amt / total) * 100 for amt in amounts]

    plt.clear_figure()
    plt.title("🥧 Payment Method Distribution")
    
    # Create bar chart
    plt.simple_bar(methods, amounts, width=0.3, title="Payment Method Spending")
    
    # Display percentages in console
    print("\n💳 Payment Method Distribution:")
    print("-" * 50)
    for method, amt, pct in zip(methods, amounts, percentages):
        bar_length = int(pct / 2)
        bar = "█" * bar_length
        print(f"{method:20s} {bar:25s} ₹{amt:>10.2f} ({pct:>5.1f}%)")
    print("-" * 50)
    print(f"{'TOTAL':20s} {' ':25s} ₹{total:>10.2f} (100.0%)")


def income_vs_expense_comparison(user):
    """
    Display income vs expense comparison chart.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Get monthly income and expenses
    cursor.execute(
        """
        SELECT 
            TO_CHAR(expense_date, 'YYYY-MM') as month,
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expense
        FROM expenses
        WHERE user_id = %s
        GROUP BY month
        ORDER BY month;
        """,
        (user["user_id"],)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print("ℹ️ No data available for income vs expense comparison.")
        return

    months = [row[0] for row in rows]
    incomes = [float(row[1]) for row in rows]
    expenses = [float(row[2]) for row in rows]

    plt.clear_figure()
    plt.title("📊 Income vs Expense Comparison")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    
    # Plot both lines
    plt.plot(months, incomes, label="Income", marker="dot")
    plt.plot(months, expenses, label="Expense", marker="dot")
    plt.show()
    
    # Display summary table
    print("\n📊 Monthly Income vs Expense:")
    print("-" * 70)
    print(f"{'Month':10s} {'Income':>15s} {'Expense':>15s} {'Savings':>15s} {'Status':>10s}")
    print("-" * 70)
    
    for month, income, expense in zip(months, incomes, expenses):
        savings = income - expense
        status = "✅ Saved" if savings >= 0 else "❌ Deficit"
        print(f"{month:10s} ₹{income:>13.2f} ₹{expense:>13.2f} ₹{savings:>13.2f} {status:>10s}")
    
    print("-" * 70)
    total_income = sum(incomes)
    total_expense = sum(expenses)
    total_savings = total_income - total_expense
    print(f"{'TOTAL':10s} ₹{total_income:>13.2f} ₹{total_expense:>13.2f} ₹{total_savings:>13.2f}")
    print("-" * 70)

