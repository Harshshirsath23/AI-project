import secrets
import hashlib
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

# Configure Argon2id password hashing engine
pwd_hash = PasswordHash((Argon2Hasher(),))

def hash_password(password: str) -> str:
    """Hashes a plain-text password using Argon2id."""
    return pwd_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against an Argon2id hash."""
    try:
        return pwd_hash.verify(plain_password, hashed_password)
    except Exception:
        return False

def generate_random_token(length: int = 32) -> str:
    """Generates a cryptographically secure random url-safe token string."""
    return secrets.token_urlsafe(length)

def hash_token(token: str) -> str:
    """Computes a SHA-256 hash of a raw token for secure database storage."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
