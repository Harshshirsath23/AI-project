import secrets
from typing import Optional

from passlib.context import CryptContext

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(length)


def generate_reset_token() -> str:
    """Generate a password reset token."""
    return secrets.token_urlsafe(48)


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > 128:
        return False, "Password must not exceed 128 characters"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    # Check for common weak passwords
    weak_passwords = {
        "password", "12345678", "qwerty123", "abc12345",
        "password123", "admin123", "welcome123"
    }
    if password.lower() in weak_passwords:
        return False, "Password is too common. Please choose a stronger password"
    
    return True, None
