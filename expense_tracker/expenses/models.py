from dataclasses import dataclass
from datetime import date
from typing import Optional


ALLOWED_TYPES = {"income", "expense"}
ALLOWED_PAYMENT_METHODS = {"cash", "upi", "card", "netbanking"}


@dataclass
class Expense:
    user_id: str
    type: str
    amount: float
    category: str
    expense_date: date
    description: Optional[str] = None
    payment_method: Optional[str] = None
    receiver: Optional[str] = None

    def validate(self):
        """
        Validate expense data before saving to DB.
        Raises ValueError if invalid.
        """

        if self.type not in ALLOWED_TYPES:
            raise ValueError("Type must be 'income' or 'expense'.")

        if self.amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        if not self.category:
            raise ValueError("Category is required.")

        if not isinstance(self.expense_date, date):
            raise ValueError("Invalid expense date.")

        if self.payment_method:
            if self.payment_method.lower() not in ALLOWED_PAYMENT_METHODS:
                raise ValueError(
                    f"Payment method must be one of {ALLOWED_PAYMENT_METHODS}"
                )

        if self.receiver and len(self.receiver) < 2:
            raise ValueError("Receiver name is too short.")
