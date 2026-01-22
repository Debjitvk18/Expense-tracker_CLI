from expense_tracker.db.connection import get_connection
from expense_tracker.auth.password import verify_password
from expense_tracker.core.session import save_session


def login():
    print("\n🔐 Login")
    print("-" * 15)

    identifier = input("Username or Email: ").strip()
    password = input("Password: ").strip()

    if not identifier or not password:
        print("❌ Both fields are required.")
        return None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, username, password_hash
            FROM users
            WHERE username = %s OR email = %s;
            """,
            (identifier, identifier)
        )

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            print("❌ User not found.")
            return None

        user_id, username, password_hash = user

        if not verify_password(password, password_hash):
            print("❌ Invalid password.")
            return None

        # ✅ Create session
        save_session(str(user_id), username)

        print(f"✅ Login successful. Welcome, {username}!")
        return {
            "user_id": str(user_id),
            "username": username
        }

    except Exception as e:
        print("❌ Login failed:", e)
        return None
