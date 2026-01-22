from datetime import datetime
from expense_tracker.expenses.models import Expense
from expense_tracker.db.connection import get_connection


def add_expense(user):
    print("\n➕ Add Expense / Income")
    print("-" * 30)

    try:
        type_ = input("Type (income/expense): ").strip().lower()
        amount = float(input("Amount: ").strip())
        category = input("Category: ").strip()
        description = input("Description (optional): ").strip() or None
        payment_method = input(
            "Payment Method (cash/upi/card/netbanking, optional): "
        ).strip().lower() or None

        date_input = input("Date (YYYY-MM-DD): ").strip()
        expense_date = datetime.strptime(date_input, "%Y-%m-%d").date()

        receiver = input("Receiver name (optional): ").strip() or None

        # Create Expense object
        expense = Expense(
            user_id=user["user_id"],
            type=type_,
            amount=amount,
            category=category,
            expense_date=expense_date,
            description=description,
            payment_method=payment_method,
            receiver=receiver
        )

        # Validate expense
        expense.validate()

        # Insert into DB
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO expenses
            (user_id, type, amount, category, description,
             payment_method, receiver, expense_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                expense.user_id,
                expense.type,
                expense.amount,
                expense.category,
                expense.description,
                expense.payment_method,
                expense.receiver,
                expense.expense_date
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ Expense saved successfully!")

    except ValueError as ve:
        print(f"❌ Validation error: {ve}")

    except Exception as e:
        print("❌ Failed to add expense:", e)
