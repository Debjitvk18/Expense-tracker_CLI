from expense_tracker.db.connection import get_connection
from expense_tracker.auth.password import hash_password
from expense_tracker.utils.validation import validate_email, validate_password, validate_mobile
from expense_tracker.core.session import save_session


def signup():
    print("\n🆕 Create New Account")
    print("-" * 25)

    username = input("Username: ").strip()
    mobile = input("Mobile number (optional): ").strip()
    email = input("Email: ").strip()
    password = input("Password (min 6 characters): ").strip()

    # Basic validations
    if not username or not email or not password:
        print("❌ Username, email, and password are required.")
        return None

    if len(username) < 3:
        print("❌ Username must be at least 3 characters long.")
        return None

    if not validate_email(email):
        print("❌ Invalid email format.")
        return None

    if not validate_password(password):
        print("❌ Password must be at least 6 characters.")
        return None

    if mobile and not validate_mobile(mobile):
        print("❌ Invalid mobile number format. Please enter 10-15 digits.")
        return None

    password_hash = hash_password(password)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (username, email, mobile, password_hash)
            VALUES (%s, %s, %s, %s)
            RETURNING id, username;
            """,
            (username, email, mobile if mobile else None, password_hash)
        )

        user_id, username = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()

        # Save session after successful signup
        save_session(str(user_id), username)

        print("✅ Account created successfully!")
        return {
            "user_id": str(user_id),
            "username": username
        }

    except Exception as e:
        error_message = str(e).lower()
        if "unique" in error_message and "username" in error_message:
            print("❌ Username already exists. Please choose a different username.")
        elif "unique" in error_message and "email" in error_message:
            print("❌ Email already registered. Please use a different email or login.")
        else:
            print(f"❌ Error creating account: {e}")

        return None

