from datetime import datetime, date
from expense_tracker.expenses.models import Expense
from expense_tracker.db.connection import get_connection

# Common category suggestions
COMMON_CATEGORIES = [
    "Food & Dining",
    "Transportation",
    "Shopping",
    "Bills & Utilities",
    "Entertainment",
    "Healthcare",
    "Education",
    "Groceries",
    "Rent",
    "Salary",
    "Investment",
    "Other"
]


def get_category_input():
    """
    Get category input with suggestions.
    """
    print("\n📂 Common Categories:")
    for i, cat in enumerate(COMMON_CATEGORIES, 1):
        print(f"{i}. {cat}")
    
    print(f"{len(COMMON_CATEGORIES) + 1}. Custom (type your own)")
    
    choice = input(f"\nSelect category (1-{len(COMMON_CATEGORIES) + 1}): ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(COMMON_CATEGORIES):
        return COMMON_CATEGORIES[int(choice) - 1]
    elif choice.isdigit() and int(choice) == len(COMMON_CATEGORIES) + 1:
        return input("Enter custom category: ").strip()
    else:
        print("❌ Invalid choice. Using 'Other' as category.")
        return "Other"


def get_date_input():
    """
    Get date input with validation and default to today.
    """
    today = date.today()
    date_input = input(f"Date (YYYY-MM-DD) [Press Enter for today: {today}]: ").strip()
    
    if not date_input:
        return today
    
    try:
        expense_date = datetime.strptime(date_input, "%Y-%m-%d").date()
        
        # Validate that the date is not in the future
        if expense_date > today:
            print("⚠️ Warning: Date is in the future. Using anyway.")
        
        return expense_date
    except ValueError:
        print(f"❌ Invalid date format. Using today's date: {today}")
        return today


def add_expense(user):
    print("\n➕ Add Expense / Income")
    print("-" * 30)

    try:
        # Type input with validation
        while True:
            type_ = input("Type (income/expense): ").strip().lower()
            if type_ in ['income', 'expense']:
                break
            print("❌ Invalid type. Please enter 'income' or 'expense'.")
        
        # Amount input with validation
        while True:
            try:
                amount = float(input("Amount: ").strip())
                if amount <= 0:
                    print("❌ Amount must be greater than 0.")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Category input with suggestions
        category = get_category_input()
        
        # Description (optional)
        description = input("Description (optional): ").strip() or None
        
        # Payment method with validation
        while True:
            payment_method = input(
                "Payment Method (cash/upi/card/netbanking) [optional]: "
            ).strip().lower() or None
            
            if payment_method is None or payment_method in ['cash', 'upi', 'card', 'netbanking']:
                break
            print("❌ Invalid payment method. Please choose from: cash, upi, card, netbanking")
        
        # Date input with validation and default
        expense_date = get_date_input()
        
        # Receiver (optional)
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

        print(f"\n✅ {type_.capitalize()} of ₹{amount:,.2f} saved successfully!")
        print(f"   Category: {category}")
        print(f"   Date: {expense_date}")

    except ValueError as ve:
        print(f"❌ Validation error: {ve}")

    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user.")

    except Exception as e:
        print(f"❌ Failed to add expense: {e}")
        print("Please try again or contact support if the issue persists.")

