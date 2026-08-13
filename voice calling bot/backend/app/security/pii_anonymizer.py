"""Advanced PII Anonymizer & Tokenizer for enterprise data privacy."""

import re
from typing import Tuple, Dict
from app.core.logging import get_logger

logger = get_logger(__name__)

# Advanced PII Regex Patterns
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b|\b\d{9}\b")
CREDIT_CARD_PATTERN = re.compile(r"\b(?:\d[ -]*?){13,16}\b")
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
PHONE_PATTERN = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
ADDRESS_PATTERN = re.compile(r"\b\d{1,5}\s+[A-Za-z0-9\s.,]{3,30}\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct)\b", re.IGNORECASE)
IBAN_PATTERN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{12,30}\b")
PASSPORT_PATTERN = re.compile(r"\b[A-Z0-9]{8,10}\b")
IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
API_KEY_PATTERN = re.compile(r"\b(sk_[a-zA-Z0-9]{24,}|AIzaSy[a-zA-Z0-9_-]{33})\b")


class PIIAnonymizer:
    """Advanced PII detection and reversible token placeholder mapping."""

    @classmethod
    def anonymize_text(cls, text: str) -> Tuple[str, Dict[str, str]]:
        """Scan and replace sensitive PII with structured token placeholders ([PHONE_1], [EMAIL_1], etc.)."""
        if not text:
            return "", {}

        mapping: Dict[str, str] = {}
        counter = {"ssn": 0, "card": 0, "email": 0, "phone": 0, "address": 0, "iban": 0, "ip": 0, "key": 0}
        anonymized = text

        # 1. API Keys
        def replace_key(match):
            counter["key"] += 1
            token = f"[API_KEY_{counter['key']}]"
            mapping[token] = match.group(0)
            return token
        anonymized = API_KEY_PATTERN.sub(replace_key, anonymized)

        # 2. SSN
        def replace_ssn(match):
            counter["ssn"] += 1
            token = f"[SSN_{counter['ssn']}]"
            mapping[token] = match.group(0)
            return token
        anonymized = SSN_PATTERN.sub(replace_ssn, anonymized)

        # 3. Credit Card
        def replace_card(match):
            counter["card"] += 1
            token = f"[CREDIT_CARD_{counter['card']}]"
            mapping[token] = match.group(0)
            return token
        anonymized = CREDIT_CARD_PATTERN.sub(replace_card, anonymized)

        # 4. IBAN
        def replace_iban(match):
            counter["iban"] += 1
            token = f"[IBAN_{counter['iban']}]"
            mapping[token] = match.group(0)
            return token
        anonymized = IBAN_PATTERN.sub(replace_iban, anonymized)

        # 5. Email
        def replace_email(match):
            counter["email"] += 1
            token = f"[EMAIL_{counter['email']}]"
            mapping[token] = match.group(0)
            return token
        anonymized = EMAIL_PATTERN.sub(replace_email, anonymized)

        # 6. Phone
        def replace_phone(match):
            counter["phone"] += 1
            token = f"[PHONE_{counter['phone']}]"
            mapping[token] = match.group(0)
            return token
        anonymized = PHONE_PATTERN.sub(replace_phone, anonymized)

        # 7. Address
        def replace_address(match):
            counter["address"] += 1
            token = f"[ADDRESS_{counter['address']}]"
            mapping[token] = match.group(0)
            return token
        anonymized = ADDRESS_PATTERN.sub(replace_address, anonymized)

        # 8. IP Address
        def replace_ip(match):
            counter["ip"] += 1
            token = f"[IP_ADDRESS_{counter['ip']}]"
            mapping[token] = match.group(0)
            return token
        anonymized = IP_PATTERN.sub(replace_ip, anonymized)

        if mapping:
            logger.info("PII tokens generated", count=len(mapping), categories=list(mapping.keys()))

        return anonymized, mapping

    @classmethod
    def deanonymize_text(cls, text: str, mapping: Dict[str, str]) -> str:
        """Restore token placeholders back to original values if required."""
        if not text or not mapping:
            return text

        restored = text
        for token, original in mapping.items():
            restored = restored.replace(token, original)
        return restored


pii_anonymizer = PIIAnonymizer()
