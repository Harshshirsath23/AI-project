from abc import ABC, abstractmethod
from typing import AsyncGenerator, Optional

from app.ai.models.llm import (
    LLMChatRequest,
    LLMChatResponse,
    LLMCompletionRequest,
    LLMCompletionResponse,
    LLMStreamingChunk,
)


class LLMProvider(ABC):
    """
    Abstract interface for Large Language Model providers.
    
    All LLM providers (Gemini, NVIDIA Nemotron, etc.) must implement this interface.
    This ensures provider-agnostic usage throughout the application.
    """

    @abstractmethod
    async def initialize(self, config: dict) -> None:
        """
        Initialize the LLM provider with configuration.
        
        Args:
            config: Provider-specific configuration dictionary
        """
        pass

    @abstractmethod
    async def chat_completion(
        self,
        request: LLMChatRequest,
    ) -> LLMChatResponse:
        """
        Generate a chat completion response.
        
        Args:
            request: LLM chat request with messages and parameters
        
        Returns:
            LLMChatResponse with generated message and metadata
        
        Raises:
            AIProviderError: If generation fails
        """
        pass

    @abstractmethod
    async def chat_completion_streaming(
        self,
        request: LLMChatRequest,
    ) -> AsyncGenerator[LLMStreamingChunk, None]:
        """
        Generate a chat completion with streaming output.
        
        This method yields response chunks as they become available,
        enabling real-time streaming responses.
        
        Args:
            request: LLM chat request with messages and parameters
        
        Yields:
            LLMStreamingChunk with partial response content
        
        Raises:
            AIProviderError: If streaming generation fails
        """
        pass

    @abstractmethod
    async def text_completion(
        self,
        request: LLMCompletionRequest,
    ) -> LLMCompletionResponse:
        """
        Generate a text completion response.
        
        Args:
            request: LLM text completion request with prompt and parameters
        
        Returns:
            LLMCompletionResponse with generated text and metadata
        
        Raises:
            AIProviderError: If generation fails
        """
        pass

    @abstractmethod
    async def text_completion_streaming(
        self,
        request: LLMCompletionRequest,
    ) -> AsyncGenerator[LLMStreamingChunk, None]:
        """
        Generate a text completion with streaming output.
        
        Args:
            request: LLM text completion request with prompt and parameters
        
        Yields:
            LLMStreamingChunk with partial text content
        
        Raises:
            AIProviderError: If streaming generation fails
        """
        pass

    @abstractmethod
    async def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in the given text.
        
        Args:
            text: Text to count tokens for
        
        Returns:
            int: Number of tokens
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the provider is healthy and available.
        
        Returns:
            bool: True if provider is healthy, False otherwise
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """
        Cleanup resources used by the provider.
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Get the name of the provider.
        
        Returns:
            str: Provider name (e.g., "gemini", "nemotron")
        """
        pass

    @property
    @abstractmethod
    def supports_streaming(self) -> bool:
        """
        Check if the provider supports streaming generation.
        
        Returns:
            bool: True if streaming is supported
        """
        pass

    @property
    @abstractmethod
    def supports_function_calling(self) -> bool:
        """
        Check if the provider supports function/tool calling.
        
        Returns:
            bool: True if function calling is supported
        """
        pass
