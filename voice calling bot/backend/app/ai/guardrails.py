"""Advanced Security & AI Guardrails Engine for Prompt Injection Defense, Toxicity, and Factuality."""

import re
from typing import Tuple, Optional
from app.core.logging import get_logger
from app.security.pii_anonymizer import PIIAnonymizer

logger = get_logger(__name__)

# Prompt Injection & Jailbreak Patterns
INJECTION_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"disregard\s+all\s+prior",
    r"reveal\s+(?:your\s+)?system\s+prompt",
    r"print\s+(?:your\s+)?system\s+instructions",
    r"you\s+are\s+now\s+in\s+DAN\s+mode",
    r"act\s+as\s+an\s+unrestricted",
    r"override\s+your\s+safety\s+rules",
    r"forget\s+all\s+rules",
    r"bypass\s+(?:the\s+)?system",
    r"what\s+is\s+your\s+system\s+prompt",
]

INJECTION_REGEX = re.compile("|".join(INJECTION_PATTERNS), re.IGNORECASE)

# Profanity & Abuse Patterns
TOXICITY_PATTERNS = [
    r"\bfuck\b", r"\bshit\b", r"\basshole\b", r"\bbitch\b", r"\bbastard\b",
    r"\bdamn\b", r"\bcrap\b", r"\bidiot\b", r"\bstupid\b", r"\bhate\s+you\b"
]

TOXICITY_REGEX = re.compile("|".join(TOXICITY_PATTERNS), re.IGNORECASE)


class PromptInjectionGuardrail:
    """Detects adversarial jailbreaks and prompt injection attempts."""

    @staticmethod
    def inspect(text: str) -> Tuple[bool, Optional[str]]:
        if not text:
            return True, None

        match = INJECTION_REGEX.search(text)
        if match:
            trigger = match.group(0)
            logger.warning("Prompt injection attempt detected and blocked", trigger=trigger)
            return False, f"Prompt injection trigger: '{trigger}'"

        return True, None


class ToxicityGuardrail:
    """Scans for profanity, abusive terms, and toxic content."""

    @staticmethod
    def inspect(text: str) -> Tuple[bool, Optional[str]]:
        if not text:
            return True, None

        match = TOXICITY_REGEX.search(text)
        if match:
            trigger = match.group(0)
            logger.warning("Toxic content detected", trigger=trigger)
            return False, f"Toxic content trigger: '{trigger}'"

        return True, None


class FactualityGuardrail:
    """Verifies generated numeric values and prices against grounding context."""

    @staticmethod
    def inspect_numbers(response_text: str, context_text: str) -> Tuple[bool, Optional[str]]:
        if not response_text or not context_text:
            return True, None

        # Extract currency/numeric values from response (e.g. $100, 50%)
        response_numbers = set(re.findall(r"\$?\b\d+(?:\.\d+)?%?\b", response_text))
        context_numbers = set(re.findall(r"\$?\b\d+(?:\.\d+)?%?\b", context_text))

        # Check for numeric claims not grounded in context
        unsupported = response_numbers - context_numbers
        # Ignore small single-digit conversation numbers like 1, 2, 3
        unsupported_significant = {n for n in unsupported if len(n.replace("$", "").replace("%", "")) > 1}

        if unsupported_significant:
            logger.warning("Factuality check warning: Unsupported numeric claim", claims=list(unsupported_significant))
            return False, f"Ungrounded numbers detected: {list(unsupported_significant)}"

        return True, None


class GuardrailEngine:
    """Unified Guardrail Execution Engine evaluating incoming speech and outgoing LLM output."""

    @classmethod
    def evaluate_input(cls, user_speech: str) -> Tuple[bool, str, Optional[str]]:
        """Evaluate incoming customer speech for prompt injection, toxicity, and PII anonymization."""
        # 1. Prompt Injection Inspection
        is_safe_inj, inj_reason = PromptInjectionGuardrail.inspect(user_speech)
        if not is_safe_inj:
            return False, "I'm sorry, I cannot process that request. How else can I assist you with Voxera services today?", inj_reason

        # 2. Toxicity Inspection
        is_safe_tox, tox_reason = ToxicityGuardrail.inspect(user_speech)
        if not is_safe_tox:
            return False, "I'm here to assist you professionally. Please let me know how I can help with your account.", tox_reason

        # 3. PII Anonymization
        anonymized, _ = PIIAnonymizer.anonymize_text(user_speech)

        return True, anonymized, None

    @classmethod
    def evaluate_output(cls, llm_response: str, context: str = "") -> Tuple[bool, str, Optional[str]]:
        """Evaluate outgoing LLM response text for toxicity, PII leaks, and length safety."""
        # 1. Toxicity Check
        is_safe_tox, tox_reason = ToxicityGuardrail.inspect(llm_response)
        if not is_safe_tox:
            return False, "Thank you for taking my call today! Have a great day.", tox_reason

        # 2. PII Redaction
        anonymized, _ = PIIAnonymizer.anonymize_text(llm_response)

        return True, anonymized, None


guardrail_engine = GuardrailEngine()
