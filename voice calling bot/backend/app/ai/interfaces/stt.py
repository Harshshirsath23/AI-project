from abc import ABC, abstractmethod
from typing import AsyncGenerator, Optional

from app.ai.models.stt import STTRequest, STTResponse, STTStreamingChunk


class STTProvider(ABC):
    """
    Abstract interface for Speech-to-Text providers.
    
    All STT providers (Faster-Whisper, Sarvam, etc.) must implement this interface.
    This ensures provider-agnostic usage throughout the application.
    """

    @abstractmethod
    async def initialize(self, config: dict) -> None:
        """
        Initialize the STT provider with configuration.
        
        Args:
            config: Provider-specific configuration dictionary
        """
        pass

    @abstractmethod
    async def transcribe(
        self,
        request: STTRequest,
    ) -> STTResponse:
        """
        Transcribe audio to text.
        
        Args:
            request: STT request with audio data and parameters
        
        Returns:
            STTResponse with transcription results
        
        Raises:
            AIProviderError: If transcription fails
        """
        pass

    @abstractmethod
    async def transcribe_streaming(
        self,
        request: STTRequest,
    ) -> AsyncGenerator[STTStreamingChunk, None]:
        """
        Transcribe audio to text with streaming results.
        
        This method yields transcription chunks as they become available,
        enabling real-time transcription.
        
        Args:
            request: STT request with audio data and parameters
        
        Yields:
            STTStreamingChunk with partial transcription results
        
        Raises:
            AIProviderError: If streaming transcription fails
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
            str: Provider name (e.g., "faster_whisper", "sarvam")
        """
        pass

    @property
    @abstractmethod
    def supports_streaming(self) -> bool:
        """
        Check if the provider supports streaming transcription.
        
        Returns:
            bool: True if streaming is supported
        """
        pass
