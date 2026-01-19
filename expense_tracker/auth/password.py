import bcrypt


def hash_password(password: str) -> str:
    """
    Takes a plain-text password and returns a hashed password.
    """
    if not password:
        raise ValueError("Password cannot be empty")

    # Convert to bytes
    password_bytes = password.encode("utf-8")

    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Store hash as string
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a stored hash.
    """
    if not password or not hashed_password:
        return False

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
