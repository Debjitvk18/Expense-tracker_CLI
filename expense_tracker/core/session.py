import json
from expense_tracker.core.config import SESSION_FILE


def save_session(user_id: str, username: str):
    data = {
        "user_id": user_id,
        "username": username
    }
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)


def load_session():
    if not SESSION_FILE.exists():
        return None

    with open(SESSION_FILE, "r") as f:
        return json.load(f)


def clear_session():
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()
