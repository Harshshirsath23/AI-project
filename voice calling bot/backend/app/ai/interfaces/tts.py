from abc import ABC, abstractmethod
from typing import AsyncGenerator

from app.ai.models.tts import TTSRequest, TTSResponse, TTSStreamingChunk


class TTSProvider(ABC):
    """
    Abstract interface for Text-to-Speech providers.
    
    All TTS providers (Piper, Sarvam, etc.) must implement this interface.
    This ensures provider-agnostic usage throughout the application.
    """

    @abstractmethod
    async def initialize(self, config: dict) -> None:
        """
        Initialize the TTS provider with configuration.
        
        Args:
            config: Provider-specific configuration dictionary
        """
        pass

    @abstractmethod
    async def synthesize(
        self,
        request: TTSRequest,
    ) -> TTSResponse:
        """
        Synthesize text to speech audio.
        
        Args:
            request: TTS request with text and voice parameters
        
        Returns:
            TTSResponse with audio data and metadata
        
        Raises:
            AIProviderError: If synthesis fails
        """
        pass

    @abstractmethod
    async def synthesize_streaming(
        self,
        request: TTSRequest,
    ) -> AsyncGenerator[TTSStreamingChunk, None]:
        """
        Synthesize text to speech with streaming audio output.
        
        This method yields audio chunks as they become available,
        enabling real-time audio playback.
        
        Args:
            request: TTS request with text and voice parameters
        
        Yields:
            TTSStreamingChunk with partial audio data
        
        Raises:
            AIProviderError: If streaming synthesis fails
        """
        pass

    @abstractmethod
    async def get_available_voices(self) -> list[dict]:
        """
        Get list of available voices for the provider.
        
        Returns:
            List of voice dictionaries with voice_id, name, language, etc.
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
            str: Provider name (e.g., "piper", "sarvam")
        """
        pass

    @property
    @abstractmethod
    def supports_streaming(self) -> bool:
        """
        Check if the provider supports streaming synthesis.
        
        Returns:
            bool: True if streaming is supported
        """
        pass
