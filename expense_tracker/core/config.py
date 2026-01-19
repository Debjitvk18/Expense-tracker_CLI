# expense_tracker/core/config.py
from pathlib import Path
import os

APP_DIR = Path.home() / ".expense_tracker"
APP_DIR.mkdir(exist_ok=True)

SESSION_FILE = APP_DIR / "session.json"

DATABASE_URL = os.getenv("DATABASE_URL")
