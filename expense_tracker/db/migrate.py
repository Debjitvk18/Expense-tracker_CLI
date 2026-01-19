from expense_tracker.db.connection import get_connection

CREATE_USERS_TABLE = """
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mobile VARCHAR(15),
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_EXPENSES_TABLE = """
CREATE TABLE IF NOT EXISTS expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(10) CHECK (type IN ('income','expense')),
    amount NUMERIC(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    payment_method VARCHAR(20),
    receiver VARCHAR(100),
    expense_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def migrate():
    conn = get_connection()
    cursor = conn.cursor()

    print("🚀 Starting database migration...")

    cursor.execute(CREATE_USERS_TABLE)
    cursor.execute(CREATE_EXPENSES_TABLE)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Database migration completed successfully.")

if __name__ == "__main__":
    migrate()
