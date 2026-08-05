"""
Standardized AI exceptions for the AI Provider Abstraction Layer.

All AI-related exceptions should inherit from AIProviderError to ensure
consistent error handling across the application. Business modules should
catch these exceptions rather than provider-specific exceptions.
"""


class AIProviderError(Exception):
    """
    Base exception for all AI provider errors.
    
    This is the base exception that all AI provider errors should inherit from.
    Business modules should catch this exception to handle any AI-related errors.
    """

    def __init__(self, message: str, provider: str = None, details: dict = None):
        """
        Initialize AI provider error.
        
        Args:
            message: Error message
            provider: Optional provider name
            details: Optional additional error details
        """
        self.message = message
        self.provider = provider
        self.details = details or {}
        super().__init__(self.message)


class ProviderUnavailableError(AIProviderError):
    """
    Raised when an AI provider is unavailable or unreachable.
    
    This could be due to network issues, service downtime, or other
    connectivity problems.
    """

    def __init__(self, message: str, provider: str = None, retry_after: int = None):
        """
        Initialize provider unavailable error.
        
        Args:
            message: Error message
            provider: Provider name
            retry_after: Optional seconds to wait before retry
        """
        super().__init__(message, provider)
        self.retry_after = retry_after


class ProviderTimeoutError(AIProviderError):
    """
    Raised when an AI provider request times out.
    
    This occurs when the provider takes longer than the configured timeout
    to respond.
    """

    def __init__(self, message: str, provider: str = None, timeout_seconds: float = None):
        """
        Initialize provider timeout error.
        
        Args:
            message: Error message
            provider: Provider name
            timeout_seconds: Timeout duration that was exceeded
        """
        super().__init__(message, provider)
        self.timeout_seconds = timeout_seconds


class ProviderRateLimitError(AIProviderError):
    """
    Raised when an AI provider rate limit is exceeded.
    
    This occurs when the provider has received too many requests within
    a time window.
    """

    def __init__(
        self,
        message: str,
        provider: str = None,
        retry_after: int = None,
        limit: int = None,
        window: str = None,
    ):
        """
        Initialize provider rate limit error.
        
        Args:
            message: Error message
            provider: Provider name
            retry_after: Seconds to wait before retry
            limit: Rate limit that was exceeded
            window: Time window for the rate limit
        """
        super().__init__(message, provider)
        self.retry_after = retry_after
        self.limit = limit
        self.window = window


class ProviderConfigurationError(AIProviderError):
    """
    Raised when provider configuration is invalid or missing.
    
    This occurs when required configuration is missing or invalid.
    """

    def __init__(self, message: str, provider: str = None, config_key: str = None):
        """
        Initialize provider configuration error.
        
        Args:
            message: Error message
            provider: Provider name
            config_key: Configuration key that caused the error
        """
        super().__init__(message, provider)
        self.config_key = config_key


class ProviderFailureError(AIProviderError):
    """
    Raised when an AI provider fails to process a request.
    
    This is a general error for provider-side failures that don't fit
    into more specific categories.
    """

    def __init__(self, message: str, provider: str = None, error_code: str = None):
        """
        Initialize provider failure error.
        
        Args:
            message: Error message
            provider: Provider name
            error_code: Optional error code from provider
        """
        super().__init__(message, provider)
        self.error_code = error_code


class UnsupportedProviderError(AIProviderError):
    """
    Raised when attempting to use an unsupported or unregistered provider.
    
    This occurs when a provider ID is not registered in the registry.
    """

    def __init__(self, message: str, provider: str = None, available_providers: list = None):
        """
        Initialize unsupported provider error.
        
        Args:
            message: Error message
            provider: Provider ID that was requested
            available_providers: List of available provider IDs
        """
        super().__init__(message, provider)
        self.available_providers = available_providers or []


class StreamingInterruptedError(AIProviderError):
    """
    Raised when a streaming AI operation is interrupted.
    
    This occurs when a streaming operation is cancelled or fails
    mid-stream.
    """

    def __init__(self, message: str, provider: str = None, chunks_received: int = 0):
        """
        Initialize streaming interrupted error.
        
        Args:
            message: Error message
            provider: Provider name
            chunks_received: Number of chunks received before interruption
        """
        super().__init__(message, provider)
        self.chunks_received = chunks_received


class InvalidRequestError(AIProviderError):
    """
    Raised when the request to an AI provider is invalid.
    
    This occurs when request parameters are invalid or malformed.
    """

    def __init__(self, message: str, provider: str = None, field: str = None):
        """
        Initialize invalid request error.
        
        Args:
            message: Error message
            provider: Provider name
            field: Request field that caused the error
        """
        super().__init__(message, provider)
        self.field = field


class ModelNotAvailableError(AIProviderError):
    """
    Raised when a requested model is not available on the provider.
    
    This occurs when a specific model is requested but not available
    for the provider.
    """

    def __init__(self, message: str, provider: str = None, model: str = None):
        """
        Initialize model not available error.
        
        Args:
            message: Error message
            provider: Provider name
            model: Model that was requested
        """
        super().__init__(message, provider)
        self.model = model


class QuotaExceededError(AIProviderError):
    """
    Raised when provider quota is exceeded.
    
    This occurs when the provider's quota (e.g., token limit, API calls)
    has been exceeded.
    """

    def __init__(self, message: str, provider: str = None, quota_type: str = None):
        """
        Initialize quota exceeded error.
        
        Args:
            message: Error message
            provider: Provider name
            quota_type: Type of quota that was exceeded
        """
        super().__init__(message, provider)
        self.quota_type = quota_type
