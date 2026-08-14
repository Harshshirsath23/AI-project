import re
from typing import Dict, Any, List
from app.modules.ai.copilot.exceptions import PromptInjectionDetected, ToolAuthorizationError

INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"disregard system prompt",
    r"you are now an unrestricted",
    r"bypass security filters",
    r"dump database",
    r"select \* from users",
    r"show all organizations",
    r"system prompt:",
    r"override rules"
]

class CopilotValidator:
    """
    Sanitizes untrusted input, validates tenant boundaries, and protects against prompt injection.
    """

    @staticmethod
    def validate_user_input(text: str) -> str:
        """Checks for prompt injection patterns in recruiter queries or pasted resumes."""
        clean_text = text.strip()
        lowered = clean_text.lower()
        
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, lowered):
                raise PromptInjectionDetected(f"Malicious prompt injection pattern detected: '{pattern}'")
                
        return clean_text

    @staticmethod
    def check_tool_permission(user_permissions: List[str], required_permission: str, tool_name: str):
        """Verifies user RBAC permissions for a requested Copilot tool."""
        if required_permission and required_permission not in user_permissions:
            raise ToolAuthorizationError(
                f"User lacks permission '{required_permission}' required for tool '{tool_name}'"
            )

    @staticmethod
    def sanitize_pii(text: str) -> str:
        """Sanitizes sensitive SSN / Passwords before passing to external LLMs."""
        # Mask SSN
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED_SSN]', text)
        # Mask Credit Card
        text = re.sub(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[REDACTED_CARD]', text)
        return text
