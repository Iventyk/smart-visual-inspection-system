"""Auth security regression tests."""

from app.core.security import get_password_hash, verify_password


def test_password_hash_supports_long_passwords() -> None:
    """Hashing should support passwords longer than bcrypt's 72-byte limit."""
    password = "p" * 200

    hashed = get_password_hash(password)

    assert verify_password(password, hashed)
