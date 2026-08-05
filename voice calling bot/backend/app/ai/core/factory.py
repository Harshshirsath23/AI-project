from typing import Optional

from app.ai.core.registry import get_registry
from app.ai.interfaces.embedding import EmbeddingProvider
from app.ai.interfaces.llm import LLMProvider
from app.ai.interfaces.stt import STTProvider
from app.ai.interfaces.tts import TTSProvider
from app.core.logging import get_logger

logger = get_logger(__name__)


class ProviderFactory:
    """
    Factory for creating AI provider instances.
    
    This factory is responsible for instantiating and configuring providers
    based on the registry and configuration. It supports dependency injection
    and allows for easy switching between providers.
    """

    def __init__(self):
        """Initialize the provider factory."""
        self._registry = get_registry()
        self._stt_instances: dict = {}
        self._tts_instances: dict = {}
        self._llm_instances: dict = {}
        self._embedding_instances: dict = {}

    async def create_stt_provider(
        self,
        provider_id: Optional[str] = None,
        config: Optional[dict] = None,
    ) -> STTProvider:
        """
        Create and initialize an STT provider instance.
        
        Args:
            provider_id: Optional provider ID. If not provided, uses default.
            config: Optional provider-specific configuration
        
        Returns:
            Initialized STT provider instance
        
        Raises:
            ValueError: If provider not found or initialization fails
        """
        provider_class = self._registry.get_stt_provider(provider_id)
        provider_id = provider_id or self._registry._default_stt
        
        # Check if instance already exists
        if provider_id in self._stt_instances:
            return self._stt_instances[provider_id]
        
        # Create new instance
        provider = provider_class()
        
        # Initialize with config
        if config is None:
            config = {}
        
        try:
            await provider.initialize(config)
            self._stt_instances[provider_id] = provider
            logger.info(
                "STT provider created and initialized",
                provider_id=provider_id,
                provider_name=provider.provider_name,
            )
            return provider
        except Exception as e:
            logger.error(
                "Failed to initialize STT provider",
                provider_id=provider_id,
                error=str(e),
            )
            raise ValueError(f"Failed to initialize STT provider: {e}")

    async def create_tts_provider(
        self,
        provider_id: Optional[str] = None,
        config: Optional[dict] = None,
    ) -> TTSProvider:
        """
        Create and initialize a TTS provider instance.
        
        Args:
            provider_id: Optional provider ID. If not provided, uses default.
            config: Optional provider-specific configuration
        
        Returns:
            Initialized TTS provider instance
        
        Raises:
            ValueError: If provider not found or initialization fails
        """
        provider_class = self._registry.get_tts_provider(provider_id)
        provider_id = provider_id or self._registry._default_tts
        
        # Check if instance already exists
        if provider_id in self._tts_instances:
            return self._tts_instances[provider_id]
        
        # Create new instance
        provider = provider_class()
        
        # Initialize with config
        if config is None:
            config = {}
        
        try:
            await provider.initialize(config)
            self._tts_instances[provider_id] = provider
            logger.info(
                "TTS provider created and initialized",
                provider_id=provider_id,
                provider_name=provider.provider_name,
            )
            return provider
        except Exception as e:
            logger.error(
                "Failed to initialize TTS provider",
                provider_id=provider_id,
                error=str(e),
            )
            raise ValueError(f"Failed to initialize TTS provider: {e}")

    async def create_llm_provider(
        self,
        provider_id: Optional[str] = None,
        config: Optional[dict] = None,
    ) -> LLMProvider:
        """
        Create and initialize an LLM provider instance.
        
        Args:
            provider_id: Optional provider ID. If not provided, uses default.
            config: Optional provider-specific configuration
        
        Returns:
            Initialized LLM provider instance
        
        Raises:
            ValueError: If provider not found or initialization fails
        """
        provider_class = self._registry.get_llm_provider(provider_id)
        provider_id = provider_id or self._registry._default_llm
        
        # Check if instance already exists
        if provider_id in self._llm_instances:
            return self._llm_instances[provider_id]
        
        # Create new instance
        provider = provider_class()
        
        # Initialize with config
        if config is None:
            config = {}
        
        try:
            await provider.initialize(config)
            self._llm_instances[provider_id] = provider
            logger.info(
                "LLM provider created and initialized",
                provider_id=provider_id,
                provider_name=provider.provider_name,
            )
            return provider
        except Exception as e:
            logger.error(
                "Failed to initialize LLM provider",
                provider_id=provider_id,
                error=str(e),
            )
            raise ValueError(f"Failed to initialize LLM provider: {e}")

    async def create_embedding_provider(
        self,
        provider_id: Optional[str] = None,
        config: Optional[dict] = None,
    ) -> EmbeddingProvider:
        """
        Create and initialize an Embedding provider instance.
        
        Args:
            provider_id: Optional provider ID. If not provided, uses default.
            config: Optional provider-specific configuration
        
        Returns:
            Initialized Embedding provider instance
        
        Raises:
            ValueError: If provider not found or initialization fails
        """
        provider_class = self._registry.get_embedding_provider(provider_id)
        provider_id = provider_id or self._registry._default_embedding
        
        # Check if instance already exists
        if provider_id in self._embedding_instances:
            return self._embedding_instances[provider_id]
        
        # Create new instance
        provider = provider_class()
        
        # Initialize with config
        if config is None:
            config = {}
        
        try:
            await provider.initialize(config)
            self._embedding_instances[provider_id] = provider
            logger.info(
                "Embedding provider created and initialized",
                provider_id=provider_id,
                provider_name=provider.provider_name,
            )
            return provider
        except Exception as e:
            logger.error(
                "Failed to initialize Embedding provider",
                provider_id=provider_id,
                error=str(e),
            )
            raise ValueError(f"Failed to initialize Embedding provider: {e}")

    async def cleanup_provider(self, provider_type: str, provider_id: str) -> None:
        """
        Cleanup a specific provider instance.
        
        Args:
            provider_type: Type of provider (stt, tts, llm, embedding)
            provider_id: ID of the provider to cleanup
        """
        instances_map = {
            "stt": self._stt_instances,
            "tts": self._tts_instances,
            "llm": self._llm_instances,
            "embedding": self._embedding_instances,
        }
        
        if provider_type not in instances_map:
            raise ValueError(f"Invalid provider type: {provider_type}")
        
        instances = instances_map[provider_type]
        
        if provider_id in instances:
            provider = instances[provider_id]
            try:
                await provider.cleanup()
                del instances[provider_id]
                logger.info(
                    "Provider cleaned up",
                    provider_type=provider_type,
                    provider_id=provider_id,
                )
            except Exception as e:
                logger.error(
                    "Failed to cleanup provider",
                    provider_type=provider_type,
                    provider_id=provider_id,
                    error=str(e),
                )

    async def cleanup_all(self) -> None:
        """
        Cleanup all provider instances.
        """
        for provider_id, provider in self._stt_instances.items():
            try:
                await provider.cleanup()
            except Exception as e:
                logger.error(
                    "Failed to cleanup STT provider",
                    provider_id=provider_id,
                    error=str(e),
                )
        
        for provider_id, provider in self._tts_instances.items():
            try:
                await provider.cleanup()
            except Exception as e:
                logger.error(
                    "Failed to cleanup TTS provider",
                    provider_id=provider_id,
                    error=str(e),
                )
        
        for provider_id, provider in self._llm_instances.items():
            try:
                await provider.cleanup()
            except Exception as e:
                logger.error(
                    "Failed to cleanup LLM provider",
                    provider_id=provider_id,
                    error=str(e),
                )
        
        for provider_id, provider in self._embedding_instances.items():
            try:
                await provider.cleanup()
            except Exception as e:
                logger.error(
                    "Failed to cleanup Embedding provider",
                    provider_id=provider_id,
                    error=str(e),
                )
        
        self._stt_instances.clear()
        self._tts_instances.clear()
        self._llm_instances.clear()
        self._embedding_instances.clear()
        
        logger.info("All providers cleaned up")


# Global factory instance
_factory = ProviderFactory()


def get_factory() -> ProviderFactory:
    """
    Get the global provider factory instance.
    
    Returns:
        ProviderFactory: The global factory
    """
    return _factory
