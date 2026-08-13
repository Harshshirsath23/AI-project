"""Quality validators and PII guardrails for voice AI output."""

import re
from typing import Tuple
from app.core.logging import get_logger

logger = get_logger(__name__)

# PII Regex Patterns
SSN_REGEX = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
CREDIT_CARD_REGEX = re.compile(r"\b(?:\d[ -]*?){13,16}\b")
EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
API_KEY_REGEX = re.compile(r"\b(sk_[a-zA-Z0-9]{24,}|AIzaSy[a-zA-Z0-9_-]{33})\b")


class ResponseValidator:
    """Validator and sanitization guardrail for LLM response strings."""

    @staticmethod
    def sanitize_pii(text: str) -> str:
        """Scan and redact PII patterns (SSNs, Credit Cards, Emails, API Keys)."""
        if not text:
            return ""

        sanitized = SSN_REGEX.sub("[redacted SSN]", text)
        sanitized = CREDIT_CARD_REGEX.sub("[redacted card]", sanitized)
        sanitized = EMAIL_REGEX.sub("[redacted email]", sanitized)
        sanitized = API_KEY_REGEX.sub("[redacted key]", sanitized)

        if sanitized != text:
            logger.warning("PII detected and redacted from AI response", original_len=len(text))

        return sanitized

    @staticmethod
    def validate_response_length(
        text: str,
        max_sentences: int = 3,
        max_chars: int = 200,
    ) -> str:
        """Enforce voice response brevity (max 3 sentences / ~200 chars)."""
        if not text:
            return ""

        cleaned = text.strip()

        # Split sentences using punctuation
        sentences = re.split(r"(?<=[.!?])\s+", cleaned)
        if len(sentences) > max_sentences:
            cleaned = " ".join(sentences[:max_sentences])

        if len(cleaned) > max_chars:
            # Cut at nearest word boundary before max_chars
            truncated = cleaned[:max_chars].rsplit(" ", 1)[0]
            cleaned = truncated + ("." if not truncated.endswith((".", "!", "?")) else "")

        return cleaned

    @classmethod
    def validate_and_format(cls, text: str) -> str:
        """Full validation pipeline: PII redaction and length trimming."""
        sanitized = cls.sanitize_pii(text)
        formatted = cls.validate_response_length(sanitized)
        return formatted


def validate_ai_response(text: str) -> str:
    """Convenience functional wrapper."""
    return ResponseValidator.validate_and_format(text)
