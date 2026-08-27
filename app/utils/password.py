import bcrypt


def hash_password(plain_password: str) -> str:
    """Hash a plain-text password using bcrypt and return it as a string."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(
        plain_password.encode("utf-8"),
        salt
    )
    return hashed.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """Check a plain-text password against a bcrypt hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False

