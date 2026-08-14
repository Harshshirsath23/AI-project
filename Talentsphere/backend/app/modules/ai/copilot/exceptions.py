"""
Copilot-specific Exception Classes
"""

class CopilotException(Exception):
    """Base exception for Copilot engine."""
    pass

class IntentClassificationError(CopilotException):
    """Raised when intent detection fails or lacks confidence."""
    pass

class ToolAuthorizationError(CopilotException):
    """Raised when user lacks permissions for requested Copilot tool."""
    pass

class CopilotStateMutationError(CopilotException):
    """Raised when LLM attempts illegal state mutation."""
    pass

class PromptInjectionDetected(CopilotException):
    """Raised when untrusted content contains malicious prompt injection."""
    pass
