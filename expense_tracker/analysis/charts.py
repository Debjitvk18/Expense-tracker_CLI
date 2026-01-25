import plotext as plt
from expense_tracker.db.connection import get_connection


def daily_expense_line_chart(user):
    """
    Display daily expense trend as ASCII line chart.
    """
    try:
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

        # Format dates as strings and amounts
        dates = [row[0].strftime('%Y-%m-%d') for row in rows]
        amounts = [float(row[1]) for row in rows]

        # Show data summary
        print("\n📈 Daily Expense Trend")
        print("=" * 60)
        print(f"Showing data from {dates[0]} to {dates[-1]}")
        print(f"Total days: {len(dates)} | Total spent: ₹{sum(amounts):,.2f}")
        print("=" * 60)
        
        # Simple text-based chart
        max_amount = max(amounts)
        for date, amount in zip(dates, amounts):
            bar_width = int((amount / max_amount) * 40) if max_amount > 0 else 0
            bar = "█" * bar_width
            print(f"{date} {bar} ₹{amount:>10,.2f}")
        print("=" * 60)
        print()
        
    except Exception as e:
        print(f"❌ Error displaying chart: {e}")


def monthly_expense_line_chart(user):
    """
    Display monthly expense trend as ASCII line chart.
    """
    try:
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
            print("ℹ️ No data available for monthly chart.")
            return

        # Group by month in Python
        from collections import defaultdict
        monthly_data = defaultdict(float)
        
        for date_obj, amount in rows:
            # Format as YYYY-MM
            month_key = date_obj.strftime('%Y-%m')
            monthly_data[month_key] += float(amount)
        
        # Sort by month
        months = sorted(monthly_data.keys())
        amounts = [monthly_data[month] for month in months]

        # Show data summary
        print("\n📈 Monthly Expense Trend")
        print("=" * 60)
        print(f"Showing data from {months[0]} to {months[-1]}")
        print(f"Total months: {len(months)} | Total spent: ₹{sum(amounts):,.2f}")
        print("=" * 60)
        
        # Simple text-based chart
        max_amount = max(amounts)
        for month, amount in zip(months, amounts):
            bar_width = int((amount / max_amount) * 40) if max_amount > 0 else 0
            bar = "█" * bar_width
            print(f"{month}   {bar} ₹{amount:>10,.2f}")
        print("=" * 60)
        print()
        
    except Exception as e:
        print(f"❌ Error displaying chart: {e}")


def category_spending_bar_chart(user):
    """
    Display category-wise spending as ASCII bar chart.
    """
    try:
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
        plt.bar(categories, amounts, orientation="horizontal")
        plt.ylabel("Category")
        plt.xlabel("Amount (₹)")
        plt.show()
        
    except Exception as e:
        print(f"❌ Error displaying chart: {e}")


def category_spending_pie_chart(user):
    """
    Display category-wise spending distribution as pie chart.
    """
    try:
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

        # Display percentages in console as visual pie chart
        print("\n🥧 Category Distribution (Pie Chart)")
        print("=" * 60)
        for cat, amt, pct in zip(categories, amounts, percentages):
            bar_length = int(pct / 2)  # Scale down for display
            bar = "█" * bar_length
            print(f"{cat:20s} {bar:25s} ₹{amt:>10,.2f} ({pct:>5.1f}%)")
        print("=" * 60)
        print(f"{'TOTAL':20s} {' ':25s} ₹{total:>10,.2f} (100.0%)")
        print()
        
    except Exception as e:
        print(f"❌ Error displaying pie chart: {e}")


def payment_method_pie_chart(user):
    """
    Display payment method distribution as pie chart.
    """
    try:
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

        # Display percentages in console as visual pie chart
        print("\n💳 Payment Method Distribution (Pie Chart)")
        print("=" * 60)
        for method, amt, pct in zip(methods, amounts, percentages):
            bar_length = int(pct / 2)
            bar = "█" * bar_length
            print(f"{method:20s} {bar:25s} ₹{amt:>10,.2f} ({pct:>5.1f}%)")
        print("=" * 60)
        print(f"{'TOTAL':20s} {' ':25s} ₹{total:>10,.2f} (100.0%)")
        print()
        
    except Exception as e:
        print(f"❌ Error displaying pie chart: {e}")


def income_vs_expense_comparison(user):
    """
    Display income vs expense comparison chart.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get all transactions
        cursor.execute(
            """
            SELECT 
                expense_date,
                type,
                amount
            FROM expenses
            WHERE user_id = %s
            ORDER BY expense_date;
            """,
            (user["user_id"],)
        )

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            print("ℹ️ No data available for income vs expense comparison.")
            return

        # Group by month in Python
        from collections import defaultdict
        monthly_income = defaultdict(float)
        monthly_expense = defaultdict(float)
        
        for date_obj, trans_type, amount in rows:
            # Format as YYYY-MM
            month_key = date_obj.strftime('%Y-%m')
            if trans_type == 'income':
                monthly_income[month_key] += float(amount)
            elif trans_type == 'expense':
                monthly_expense[month_key] += float(amount)
        
        # Get all unique months and sort
        all_months = sorted(set(list(monthly_income.keys()) + list(monthly_expense.keys())))
        
        if not all_months:
            print("ℹ️ No data available for income vs expense comparison.")
            return
        
        # Build data for display
        incomes = [monthly_income[month] for month in all_months]
        expenses = [monthly_expense[month] for month in all_months]
        
        # Display summary table
        print("\n📊 Income vs Expense Comparison")
        print("=" * 80)
        print(f"{'Month':10s} {'Income':>15s} {'Expense':>15s} {'Savings':>15s} {'Status':>12s}")
        print("=" * 80)
        
        for month in all_months:
            income = monthly_income[month]
            expense = monthly_expense[month]
            savings = income - expense
            status = "✅ Saved" if savings >= 0 else "❌ Deficit"
            print(f"{month:10s} ₹{income:>13,.2f} ₹{expense:>13,.2f} ₹{savings:>13,.2f} {status:>12s}")
        
        print("=" * 80)
        total_income = sum(incomes)
        total_expense = sum(expenses)
        total_savings = total_income - total_expense
        print(f"{'TOTAL':10s} ₹{total_income:>13,.2f} ₹{total_expense:>13,.2f} ₹{total_savings:>13,.2f}")
        print("=" * 80)
        
        # Visual comparison bars
        print("\n📊 Visual Comparison:")
        print("=" * 80)
        max_value = max(max(incomes) if incomes else 0, max(expenses) if expenses else 0)
        
        for month in all_months:
            income = monthly_income[month]
            expense = monthly_expense[month]
            
            # Calculate bar widths (max 30 characters)
            income_bar_width = int((income / max_value) * 30) if max_value > 0 else 0
            expense_bar_width = int((expense / max_value) * 30) if max_value > 0 else 0
            
            print(f"\n{month}:")
            print(f"  Income:  {'█' * income_bar_width} ₹{income:,.2f}")
            print(f"  Expense: {'█' * expense_bar_width} ₹{expense:,.2f}")
        
        print("\n" + "=" * 80)
        print()
        
    except Exception as e:
        print(f"❌ Error displaying comparison: {e}")




