from expense_tracker.db.connection import get_connection


def filter_by_date_range(user_id, start_date, end_date):
    """
    Fetch expenses between start_date and end_date (inclusive).
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            expense_date,
            type,
            category,
            amount,
            payment_method,
            receiver,
            description
        FROM expenses
        WHERE user_id = %s
          AND expense_date BETWEEN %s AND %s
        ORDER BY expense_date DESC;
        """,
        (user_id, start_date, end_date)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def filter_by_category(user_id, category):
    """
    Fetch expenses for a specific category.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            expense_date,
            type,
            category,
            amount,
            payment_method,
            receiver,
            description
        FROM expenses
        WHERE user_id = %s
          AND category = %s
        ORDER BY expense_date DESC;
        """,
        (user_id, category)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def filter_by_amount_range(user_id, min_amount, max_amount):
    """
    Fetch expenses within an amount range.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            expense_date,
            type,
            category,
            amount,
            payment_method,
            receiver,
            description
        FROM expenses
        WHERE user_id = %s
          AND amount BETWEEN %s AND %s
        ORDER BY expense_date DESC;
        """,
        (user_id, min_amount, max_amount)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
