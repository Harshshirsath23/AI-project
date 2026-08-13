"""Field-level symmetric encryption service powered by Fernet (AES-128 in CBC mode with HMAC)."""

import base64
import hashlib
from typing import Optional
from cryptography.fernet import Fernet
from app.config.settings import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class EncryptionService:
    """Symmetric encryption service for protecting API keys, tokens, and confidential strings."""

    def __init__(self, key: Optional[str] = None):
        settings = get_settings()
        raw_key = key or settings.encryption_key

        if not raw_key:
            # Derive valid 32-byte URL-safe base64 key from secret_key if encryption_key is unset
            derived = hashlib.sha256(settings.secret_key.encode()).digest()
            raw_key = base64.urlsafe_b64encode(derived).decode()

        try:
            self.cipher = Fernet(raw_key.encode() if isinstance(raw_key, str) else raw_key)
        except Exception as e:
            logger.error("Failed to initialize Fernet cipher", error=str(e))
            # Fallback key generation
            derived = hashlib.sha256(settings.secret_key.encode()).digest()
            fallback_key = base64.urlsafe_b64encode(derived)
            self.cipher = Fernet(fallback_key)

    def encrypt(self, plain_text: Optional[str]) -> Optional[str]:
        """Encrypt plain text string to ciphertext."""
        if not plain_text:
            return None
        try:
            encrypted_bytes = self.cipher.encrypt(plain_text.encode("utf-8"))
            return encrypted_bytes.decode("utf-8")
        except Exception as e:
            logger.error("Encryption failure", error=str(e))
            raise ValueError("Failed to encrypt data") from e

    def decrypt(self, cipher_text: Optional[str]) -> Optional[str]:
        """Decrypt ciphertext back to plain text."""
        if not cipher_text:
            return None
        try:
            decrypted_bytes = self.cipher.decrypt(cipher_text.encode("utf-8"))
            return decrypted_bytes.decode("utf-8")
        except Exception as e:
            logger.error("Decryption failure", error=str(e))
            return None


def get_encryption_service() -> EncryptionService:
    """Get singleton instance of EncryptionService."""
    return EncryptionService()
