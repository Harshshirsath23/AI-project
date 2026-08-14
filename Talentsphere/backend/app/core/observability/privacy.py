import re
from typing import Any, Dict, List, Set

# Sensitive keys that must ALWAYS be redacted from traces
SENSITIVE_KEYS: Set[str] = {
    "password", "pass", "secret", "jwt", "jwt_token", "token", "access_token",
    "refresh_token", "api_key", "apikey", "authorization", "auth",
    "credit_card", "card_number", "ssn", "private_key", "credentials", "auth_token"
}

# Regex patterns for sensitive data scrubbing
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
JWT_REGEX = re.compile(r"eyJ[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*")
API_KEY_REGEX = re.compile(r"\b(?:sk|pk|api|key)_[a-zA-Z0-9]{16,}\b", re.IGNORECASE)

REDACTED_TEXT = "[REDACTED]"
REDACTED_PAYLOAD = "[REDACTED_PAYLOAD]"


def sanitize_string(text: str) -> str:
    """Scrub sensitive credentials, tokens, emails, and phone numbers from strings."""
    if not text:
        return text
    
    text = JWT_REGEX.sub(REDACTED_TEXT, text)
    text = API_KEY_REGEX.sub(REDACTED_TEXT, text)
    text = EMAIL_REGEX.sub("[REDACTED_EMAIL]", text)
    text = PHONE_REGEX.sub("[REDACTED_PHONE]", text)
    return text


def sanitize_payload(
    payload: Any, 
    capture_content: bool = True
) -> Any:
    """
    Recursively sanitize input/output payloads before sending telemetry to LangSmith.
    Redacts passwords, tokens, API keys, and sensitive PII.
    If capture_content is False, returns a redacted summary placeholder.
    """
    if not capture_content:
        if isinstance(payload, (dict, list)):
            return REDACTED_PAYLOAD
        elif isinstance(payload, str) and len(payload) > 50:
            return f"[SUMMARY_ONLY: length={len(payload)}]"
    
    if payload is None:
        return None

    if isinstance(payload, str):
        return sanitize_string(payload)

    if isinstance(payload, (int, float, bool)):
        return payload

    if isinstance(payload, dict):
        sanitized_dict: Dict[str, Any] = {}
        for key, value in payload.items():
            key_lower = str(key).lower()
            if any(sensitive in key_lower for sensitive in SENSITIVE_KEYS):
                sanitized_dict[key] = REDACTED_TEXT
            else:
                sanitized_dict[key] = sanitize_payload(value, capture_content=capture_content)
        return sanitized_dict

    if isinstance(payload, list):
        return [sanitize_payload(item, capture_content=capture_content) for item in payload]

    if isinstance(payload, tuple):
        return tuple(sanitize_payload(item, capture_content=capture_content) for item in payload)

    # Fallback to string representation sanitized
    return sanitize_string(str(payload))


def sanitize_error_message(error: Exception | str) -> str:
    """Extract and sanitize error message string for safe trace reporting."""
    msg = str(error) if error else "Unknown Error"
    return sanitize_string(msg)
