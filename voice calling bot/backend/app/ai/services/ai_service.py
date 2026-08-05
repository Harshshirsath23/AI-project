from typing import AsyncGenerator, Optional

from app.ai.core.config import get_ai_config
from app.ai.core.exceptions import (
    AIProviderError,
    ProviderUnavailableError,
    UnsupportedProviderError,
)
from app.ai.core.factory import get_factory
from app.ai.core.observability import (
    AIObservability,
    observe_ai_operation,
    get_observability,
)
from app.ai.interfaces.embedding import EmbeddingProvider
from app.ai.interfaces.llm import LLMProvider
from app.ai.interfaces.stt import STTProvider
from app.ai.interfaces.tts import TTSProvider
from app.ai.models.embedding import EmbeddingRequest, EmbeddingResponse
from app.ai.models.llm import (
    LLMChatRequest,
    LLMChatResponse,
    LLMCompletionRequest,
    LLMCompletionResponse,
    LLMStreamingChunk,
)
from app.ai.models.stt import STTRequest, STTResponse, STTStreamingChunk
from app.ai.models.tts import TTSRequest, TTSResponse, TTSStreamingChunk
from app.core.logging import get_logger

logger = get_logger(__name__)


class AIService:
    """
    AI Service Layer - Single entry point for all AI operations.
    
    This service acts as the orchestration layer for all AI functionality.
    Business modules should only communicate with this service, never directly
    with AI providers. The service internally resolves the correct provider
    based on configuration and executes the requested operation.
    
    This ensures:
    - Provider-agnostic business logic
    - Easy provider switching
    - Consistent error handling
    - Centralized logging and metrics
    """

    def __init__(self):
        """Initialize the AI service."""
        self._factory = get_factory()
        self._config = get_ai_config()
        self._observability = get_observability()

    async def _get_stt_provider(self, provider_id: Optional[str] = None) -> STTProvider:
        """Get configured STT provider instance."""
        provider_id = provider_id or self._config.default_stt_provider
        if not provider_id:
            raise AIProviderError("No STT provider configured")
        
        provider_config = self._config.get_stt_config(provider_id)
        if not/provider_config.enabled:
            raise ProviderUnavailableError(f"STT provider '{provider_id}' is disabled")
        
        self._observability.log_provider_selection(
            operation="stt_transcribe",
            provider=provider_id,
            reason="default" if provider_id == self._config.default_stt_provider else "override",
        )
        
        return await self._factory.create_stt_provider(provider_id, provider_config.custom_settings)

    async def _get_tts_provider(self, provider_id: Optional[str] = None) -> TTSProvider:
        """Get configured TTS provider instance."""
        provider_id = provider_id or self._config.default_tts_provider
        if not provider_id:
            raise AIProviderError("No TTS provider configured")
        
        provider_config = self._config.get_tts_config(provider_id)
        if not provider_config.enabled:
            raise ProviderUnavailableError(f"TTS provider '{provider_id}' is disabled")
        
        self._observability.log_provider_selection(
            operation="tts_synthesize",
            provider=provider_id,
            reason="default" if provider_id == self._config.default_tts_provider else "override",
        )
        
        return await self._factory.create_tts_provider(provider_id, provider_config.custom_settings)

    async def _get_llm_provider(self, provider_id: Optional[str] = None) -> LLMProvider:
        """Get configured LLM provider instance."""
        provider_id = provider_id or self._config.default_llm_provider
        if not provider_id:
            raise AIProviderError("No LLM provider configured")
        
        provider_config = self._config.get_llm_config(provider_id)
        if not provider_config.enabled:
            raise ProviderUnavailableError(f"LLM provider '{provider_id}' is disabled")
        
        self._observability.log_provider_selection(
            operation="llm_chat",
            provider=provider_id,
            reason="default" if provider_id == self._config.default_llm_provider else "override",
        )
        
        return await self._factory.create_llm_provider(provider_id, provider_config.custom_settings)

    async def _get_embedding_provider(self, provider_id: Optional[str] = None) -> EmbeddingProvider:
        """Get configured Embedding provider instance."""
        provider_id = provider_id or self._config.default_embedding_provider
        if not provider_id:
            raise AIProviderError("No Embedding provider configured")
        
        provider_config = self._config.get_embedding_config(provider_id)
        if not provider_config.enabled:
            raise ProviderUnavailableError(f"Embedding provider '{provider_id}' is disabled")
        
        self._observability.log_provider_selection(
            operation="embedding_generate",
            provider=provider_id,
            reason="default" if provider_id == self._config.default_embedding_provider else "override",
        )
        
        return await self._factory.create_embedding_provider(provider_id, provider_config.custom_settings)

    # STT Operations

    async def transcribe(
        self,
        request: STTRequest,
        provider_id: Optional[str] = None,
    ) -> STTResponse:
        """
        Transcribe audio to text.
        
        Args:
            request: STT request with audio data and parameters
            provider_id: Optional provider ID override
        
        Returns:
            STTResponse with transcription results
        
        Raises:
            AIProviderError: If transcription fails
        """
        provider = await self._get_stt_provider(provider_id)
        
        async with observe_ai_operation(
            self._observability,
            "stt_transcribe",
            provider.provider_name,
        ):
            response = await provider.transcribe(request)
            return response

    async def transcribe_streaming(
        self,
        request: STTRequest,
        provider_id: Optional[str] = None,
    ) -> AsyncGenerator[STTStreamingChunk, None]:
        """
        Transcribe audio to text with streaming results.
        
        Args:
            request: STT request with audio data and parameters
            provider_id: Optional provider ID override
        
        Yields:
            STTStreamingChunk with partial transcription results
        
        Raises:
            AIProviderError: If streaming transcription fails
        """
        provider = await self._get_stt_provider(provider_id)
        
        if not provider.supports_streaming:
            raise AIProviderError(f"Provider '{provider.provider_name}' does not support streaming")
        
        self._observability.log_streaming_start("stt_transcribe_streaming", provider.provider_name)
        
        chunk_count = 0
        try:
            async for chunk in provider.transcribe_streaming(request):
                chunk_count += 1
                self._observability.log_streaming_chunk(
                    "stt_transcribe_streaming",
                    provider.provider_name,
                    chunk_count,
                    len(chunk.text),
                )
                yield chunk
            
            self._observability.log_streaming_end(
                "stt_transcribe_streaming",
                provider.provider_name,
                chunk_count,
                0.0,  # Duration would be tracked separately
            )
        except Exception as e:
            self._observability.log_streaming_error(
                "stt_transcribe_streaming",
                provider.provider_name,
                str(e),
                chunk_count,
            )
            raise

    # TTS Operations

    async def synthesize(
        self,
        request: TTSRequest,
        provider_id: Optional[str] = None,
    ) -> TTSResponse:
        """
        Synthesize text to speech audio.
        
        Args:
            request: TTS request with text and voice parameters
            provider_id: Optional provider ID override
        
        Returns:
            TTSResponse with audio data and metadata
        
        Raises:
            AIProviderError: If synthesis fails
        """
        provider = await self._get_tts_provider(provider_id)
        
        async with observe_ai_operation(
            self._observability,
            "tts_synthesize",
            provider.provider_name,
        ):
            response = await provider.synthesize(request)
            return response

    async def synthesize_streaming(
        self,
        request: TTSRequest,
        provider_id: Optional[str] = None,
    ) -> AsyncGenerator[TTSStreamingChunk, None]:
        """
        Synthesize text to speech with streaming audio output.
        
        Args:
            request: TTS request with text and voice parameters
            provider_id: Optional provider ID override
        
        Yields:
            TTSStreamingChunk with partial audio data
        
        Raises:
            AIProviderError: If streaming synthesis fails
        """
        provider = await self._get_tts_provider(provider_id)
        
        if not provider.supports_streaming:
            raise AIProviderError(f"Provider '{provider.provider_name}' does not support streaming")
        
        self._observability.log_streaming_start("tts_synthesize_streaming", provider.provider_name)
        
        chunk_count = 0
        try:
            async for chunk in provider.synthesize_streaming(request):
                chunk_count += 1
                self._observability.log_streaming_chunk(
                    "tts_synthesize_streaming",
                    provider.provider_name,
                    chunk_count,
                    len(chunk.audio_data),
                )
                yield chunk
            
            self._observability.log_streaming_end(
                "tts_synthesize_streaming",
                provider.provider_name,
                chunk_count,
                0.0,
            )
        except Exception as e:
            self._observability.log_streaming_error(
                "tts_synthesize_streaming",
                provider.provider_name,
                str(e),
                chunk_count,
            )
            raise

    async def get_available_voices(
        self,
        provider_id: Optional[str] = None,
    ) -> list[dict]:
        """
        Get list of available voices for TTS.
        
        Args:
            provider_id: Optional provider ID override
        
        Returns:
            List of voice dictionaries
        """
        provider = await self._get_tts_provider(provider_id)
        return await provider.get_available_voices()

    # LLM Operations

    async def chat_completion(
        self,
        request: LLMChatRequest,
        provider_id: Optional[str] = None,
    ) -> LLMChatResponse:
        """
        Generate a chat completion response.
        
        Args:
            request: LLM chat request with messages and parameters
            provider_id: Optional provider ID override
        
        Returns:
            LLMChatResponse with generated message and metadata
        
        Raises:
            AIProviderError: If generation fails
        """
        provider = await self._get_llm_provider(provider_id)
        
        async with observe_ai_operation(
            self._observability,
            "llm_chat",
            provider.provider_name,
        ):
            response = await provider.chat_completion(request)
            self._observability.record_success(
                "llm_chat",
                provider.provider_name,
                response.processing_time,
                response.total_tokens,
            )
            return response

    async def chat_completion_streaming(
        self,
        request: LLMChatRequest,
        provider_id: Optional[str] = None,
    ) -> AsyncGenerator[LLMStreamingChunk, None]:
        """
        Generate a chat completion with streaming output.
        
        Args:
            request: LLM chat request with messages and parameters
            provider_id: Optional provider ID override
        
        Yields:
            LLMStreamingChunk with partial response content
        
        Raises:
            AIProviderError: If streaming generation fails
        """
        provider = await self._get_llm_provider(provider_id)
        
        if not provider.supports_streaming:
            raise AIProviderError(f"Provider '{provider.provider_name}' does not support streaming")
        
        self._observability.log_streaming_start("llm_chat_streaming", provider.provider_name)
        
        chunk_count = 0
        try:
            async for chunk in provider.chat_completion_streaming(request):
                chunk_count += 1
                self._observability.log_streaming_chunk(
                    "llm_chat_streaming",
                    provider.provider_name,
                    chunk_count,
                    len(chunk.content),
                )
                yield chunk
            
            self._observability.log_streaming_end(
                "llm_chat_streaming",
                provider.provider_name,
                chunk_count,
                0.0,
            )
        except Exception as e:
            self._observability.log_streaming_error(
                "llm_chat_streaming",
                provider.provider_name,
                str(e),
                chunk_count,
            )
            raise

    async def text_completion(
        self,
        request: LLMCompletionRequest,
        provider_id: Optional[str] = None,
    ) -> LLMCompletionResponse:
        """
        Generate a text completion response.
        
        Args:
            request: LLM text completion request with prompt and parameters
            provider_id: Optional provider ID override
        
        Returns:
            LLMCompletionResponse with generated text and metadata
        
        Raises:
            AIProviderError: If generation fails
        """
        provider = await self._get_llm_provider(provider_id)
        
        async with observe_ai_operation(
            self._observability,
            "llm_completion",
            provider.provider_name,
        ):
            response = await provider.text_completion(request)
            self._observability.record_success(
                "llm_completion",
                provider.provider_name,
                response.processing_time,
                response.total_tokens,
            )
            return response

    async def count_tokens(
        self,
        text: str,
        provider_id: Optional[str] = None,
    ) -> int:
        """
        Count the number of tokens in the given text.
        
        Args:
            text: Text to count tokens for
            provider_id: Optional provider ID override
        
        Returns:
            int: Number of tokens
        """
        provider = await self._get_llm_provider(provider_id)
        return await provider.count_tokens(text)

    # Embedding Operations

    async def generate_embedding(
        self,
        request: EmbeddingRequest,
        provider_id: Optional[str] = None,
    ) -> EmbeddingResponse:
        """
        Generate an embedding for a single text.
        
        Args:
            request: Embedding request with text and parameters
            provider_id: Optional provider ID override
        
        Returns:
            EmbeddingResponse with embedding vector and metadata
        
        Raises:
            AIProviderError: If embedding generation fails
        """
        provider = await self._get_embedding_provider(provider_id)
        
        async with observe_ai_operation(
            self._observability,
            "embedding_generate",
            provider.provider_name,
        ):
            response = await provider.generate_embedding(request)
            return response

    async def generate_embeddings_batch(
        self,
        texts: list[str],
        provider_id: Optional[str] = None,
    ) -> list[EmbeddingResponse]:
        """
        Generate embeddings for multiple texts in batch.
        
        Args:
            texts: List of texts to generate embeddings for
            provider_id: Optional provider ID override
        
        Returns:
            List of EmbeddingResponse with embedding vectors
        
        Raises:
            AIProviderError: If batch embedding generation fails
        """
        provider = await self._get_embedding_provider(provider_id)
        
        async with observe_ai_operation(
            self._observability,
            "embedding_batch",
            provider.provider_name,
        ):
            responses = await provider.generate_embeddings_batch(texts)
            return responses

    # Health Check

    async def health_check(
        self,
        provider_type: str,
        provider_id: Optional[str] = None,
    ) -> bool:
        """
        Check if a provider is healthy and available.
        
        Args:
            provider_type: Type of provider (stt, tts, llm, embedding)
            provider_id: Optional provider ID override
        
        Returns:
            bool: True if provider is healthy
        """
        try:
            if provider_type == "stt":
                provider = await self._get_stt_provider(provider_id)
            elif provider_type == "tts":
                provider = await self._get_tts_provider(provider_id)
            elif provider_type == "llm":
                provider = await self._get_llm_provider(provider_id)
            elif provider_type == "embedding":
                provider = await self._get_embedding_provider(provider_id)
            else:
                raise ValueError(f"Invalid provider type: {provider_type}")
            
            return await provider.health_check()
        except Exception as e:
            logger.error(
                "Health check failed",
                provider_type=provider_type,
                provider_id=provider_id,
                error=str(e),
            )
            return False


# Global service instance
_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    """
    Get the global AI service instance.
    
    Returns:
        AIService: The global service
    """
    global _service
    if _service is None:
        _service = AIService()
    return _service
