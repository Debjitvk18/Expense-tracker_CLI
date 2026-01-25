import re


def validate_email(email: str) -> bool:
    """
    Validate email format using regex.
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def validate_password(password: str) -> bool:
    """
    Validate password length (minimum 6 characters).
    """
    return len(password) >= 6


def validate_mobile(mobile: str) -> bool:
    """
    Validate mobile number format.
    Accepts 10-15 digits, optional + prefix, optional spaces/dashes.
    """
    if not mobile:
        return True  # Mobile is optional
    
    # Remove common separators
    cleaned = mobile.replace(" ", "").replace("-", "").replace("+", "")
    
    # Check if it's all digits and has valid length
    if cleaned.isdigit() and 10 <= len(cleaned) <= 15:
        return True
    
    return False

