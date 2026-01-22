from expense_tracker.db.connection import get_connection
from expense_tracker.auth.password import hash_password
from expense_tracker.utils.validators import validate_email, validate_password


def signup():
    print("\n🆕 Create New Account")
    print("-" * 25)

    username = input("Username: ").strip()
    mobile = input("Mobile number: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    # Basic validations
    if not username or not email or not password:
        print("❌ Username, email, and password are required.")
        return None

    if not validate_email(email):
        print("❌ Invalid email format.")
        return None

    if not validate_password(password):
        print("❌ Password must be at least 6 characters.")
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
            (username, email, mobile, password_hash)
        )

        user_id, username = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ Account created successfully!")
        return {
            "user_id": str(user_id),
            "username": username
        }

    except Exception as e:
        if "unique" in str(e).lower():
            print("❌ Username or email already exists.")
        else:
            print("❌ Error creating account:", e)

        return None
