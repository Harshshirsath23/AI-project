from typing import Dict, Optional, Type

from app.ai.interfaces.embedding import EmbeddingProvider
from app.ai.interfaces.llm import LLMProvider
from app.ai.interfaces.stt import STTProvider
from app.ai.interfaces.tts import TTSProvider
from app.core.logging import get_logger

logger = get_logger(__name__)


class ProviderRegistry:
    """
    Registry for AI providers.
    
    This registry manages the registration and resolution of AI providers.
    It allows for dynamic provider selection and switching without modifying business code.
    """

    def __init__(self):
        """Initialize the provider registry."""
        self._stt_providers: Dict[str, Type[STTProvider]] = {}
        self._tts_providers: Dict[str, Type[TTSProvider]] = {}
        self._llm_providers: Dict[str, Type[LLMProvider]] = {}
        self._embedding_providers: Dict[str, Type[EmbeddingProvider]] = {}
        
        self._default_stt: Optional[str] = None
        self._default_tts: Optional[str] = None
        self._default_llm: Optional[str] = None
        self._default_embedding: Optional[str] = None

    def register_stt_provider(
        self,
        provider_class: Type[STTProvider],
        provider_id: str,
        is_default: bool = False,
    ) -> None:
        """
        Register a Speech-to-Text provider.
        
        Args:
            provider_class: The provider class to register
            provider_id: Unique identifier for the provider
            is_default: Whether this is the default provider
        """
        self._stt_providers[provider_id] = provider_class
        if is_default or not self._default_stt:
            self._default_stt = provider_id
        logger.info(
            "STT provider registered",
            provider_id=provider_id,
            is_default=is_default,
        )

    def register_tts_provider(
        self,
        provider_class: Type[TTSProvider],
        provider_id: str,
        is_default: bool = False,
    ) -> None:
        """
        Register a Text-to-Speech provider.
        
        Args:
            provider_class: The provider class to register
            provider_id: Unique identifier for the provider
            is_default: Whether this is the default provider
        """
        self._tts_providers[provider_id] = provider_class
        if is_default or not self._default_tts:
            self._default_tts = provider_id
        logger.info(
            "TTS provider registered",
            provider_id=provider_id,
            is_default=is_default,
        )

    def register_llm_provider(
        self,
        provider_class: Type[LLMProvider],
        provider_id: str,
        is_default: bool = False,
    ) -> None:
        """
        Register a Large Language Model provider.
        
        Args:
            provider_class: The provider class to register
            provider_id: Unique identifier for the provider
            is_default: Whether this is the default provider
        """
        self._llm_providers[provider_id] = provider_class
        if is_default or not self._default_llm:
            self._default_llm = provider_id
        logger.info(
            "LLM provider registered",
            provider_id=provider_id,
            is_default=is_default,
        )

    def register_embedding_provider(
        self,
        provider_class: Type[EmbeddingProvider],
        provider_id: str,
        is_default: bool = False,
    ) -> None:
        """
        Register an Embedding provider.
        
        Args:
            provider_class: The provider class to register
            provider_id: Unique identifier for the provider
            is_default: Whether this is the default provider
        """
        self._embedding_providers[provider_id] = provider_class
        if is_default or not self._default_embedding:
            self._default_embedding = provider_id
        logger.info(
            "Embedding provider registered",
            provider_id=provider_id,
            is_default=is_default,
        )

    def get_stt_provider(self, provider_id: Optional[str] = None) -> Type[STTProvider]:
        """
        Get a registered STT provider class.
        
        Args:
            provider_id: Optional provider ID. If not provided, returns default.
        
        Returns:
            The provider class
        
        Raises:
            ValueError: If provider not found
        """
        if provider_id is None:
            provider_id = self._default_stt
        
        if provider_id not in self._stt_providers:
            raise ValueError(
                f"STT provider '{provider_id}' not registered. "
                f"Available: {list(self._stt_providers.keys())}"
            )
        
        return self._stt_providers[provider_id]

    def get_tts_provider(self, provider_id: Optional[str] = None) -> Type[TTSProvider]:
        """
        Get a registered TTS provider class.
        
        Args:
            provider_id: Optional provider ID. If not provided, returns default.
        
        Returns:
            The provider class
        
        Raises:
            ValueError: If provider not found
        """
        if provider_id is None:
            provider_id = self._default_tts
        
        if provider_id not in self._tts_providers:
            raise ValueError(
                f"TTS provider '{provider_id}' not registered. "
                f"Available: {list(self._tts_providers.keys())}"
            )
        
        return self._tts_providers[provider_id]

    def get_llm_provider(self, provider_id: Optional[str] = None) -> Type[LLMProvider]:
        """
        Get a registered LLM provider class.
        
        Args:
            provider_id: Optional provider ID. If not provided, returns default.
        
        Returns:
            The provider class
        
        Raises:
            ValueError: If provider not found
        """
        if provider_id is None:
            provider_id = self._default_llm
        
        if provider_id not in self._llm_providers:
            raise ValueError(
                f"LLM provider '{provider_id}' not registered. "
                f"Available: {list(self._llm_providers.keys())}"
            )
        
        return self._llm_providers[provider_id]

    def get_embedding_provider(
        self,
        provider_id: Optional[str] = None,
    ) -> Type[EmbeddingProvider]:
        """
        Get a registered Embedding provider class.
        
        Args:
            provider_id: Optional provider ID. If not provided, returns default.
        
        Returns:
            The provider class
        
        Raises:
            ValueError: If provider not found
        """
        if provider_id is None:
            provider_id = self._default_embedding
        
        if provider_id not in self._embedding_providers:
            raise ValueError(
                f"Embedding provider '{provider_id}' not registered. "
                f"Available: {list(self._embedding_providers.keys())}"
            )
        
        return self._embedding_providers[provider_id]

    def list_stt_providers(self) -> list[str]:
        """Get list of registered STT provider IDs."""
        return list(self._stt_providers.keys())

    def list_tts_providers(self) -> list[str]:
        """Get list of registered TTS provider IDs."""
        return list(self._tts_providers.keys())

    def list_llm_providers(self) -> list[str]:
        """Get list of registered LLM provider IDs."""
        return list(self._llm_providers.keys())

    def list_embedding_providers(self) -> list[str]:
        """Get list of registered Embedding provider IDs."""
        return list(self._embedding_providers.keys())

    def set_default_stt(self, provider_id: str) -> None:
        """
        Set the default STT provider.
        
        Args:
            provider_id: Provider ID to set as default
        
        Raises:
            ValueError: If provider not found
        """
        if provider_id not in self._stt_providers:
            raise ValueError(f"STT provider '{provider_id}' not registered")
        self._default_stt = provider_id
        logger.info("Default STT provider set", provider_id=provider_id)

    def set_default_tts(self, provider_id: str) -> None:
        """
        Set the default TTS provider.
        
        Args:
            provider_id: Provider ID to set as default
        
        Raises:
            ValueError: If provider not found
        """
        if provider_id not in self._tts_providers:
            raise ValueError(f"TTS provider '{provider_id}' not registered")
        self._default_tts = provider_id
        logger.info("Default TTS provider set", provider_id=provider_id)

    def set_default_llm(self, provider_id: str) -> None:
        """
        Set the default LLM provider.
        
        Args:
            provider_id: Provider ID to set as default
        
        Raises:
            ValueError: If provider not found
        """
        if provider_id not in self._llm_providers:
            raise ValueError(f"LLM provider '{provider_id}' not registered")
        self._default_llm = provider_id
        logger.info("Default LLM provider set", provider_id=provider_id)

    def set_default_embedding(self, provider_id: str) -> None:
        """
        Set the default Embedding provider.
        
        Args:
            provider_id: Provider ID to set as default
        
        Raises:
            ValueError: If provider not found
        """
        if provider_id not in self._embedding_providers:
            raise ValueError(f"Embedding provider '{provider_id}' not registered")
        self._default_embedding = provider_id
        logger.info("Default Embedding provider set", provider_id=provider_id)


# Global registry instance
_registry = ProviderRegistry()


def get_registry() -> ProviderRegistry:
    """
    Get the global provider registry instance.
    
    Returns:
        ProviderRegistry: The global registry
    """
    return _registry
