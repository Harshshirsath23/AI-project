from typing import Optional, Dict, Any
from dataclasses import dataclass, field

from app.config.settings import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


@dataclass
class ProviderConfig:
    """Configuration for a specific AI provider."""

    provider_id: str
    enabled: bool = True
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    streaming_enabled: bool = True
    custom_settings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIConfig:
    """
    Centralized AI configuration manager.
    
    This class manages configuration for all AI providers and operations.
    It provides a single source of truth for AI-related settings.
    """

    # Default providers
    default_stt_provider: Optional[str] = None
    default_tts_provider: Optional[str] = None
    default_llm_provider: Optional[str] = None
    default_embedding_provider: Optional[str] = None

    # Global settings
    global_timeout: float = 30.0
    global_max_retries: int = 3
    global_retry_delay: float = 1.0
    enable_streaming: bool = True

    # Provider-specific configurations
    stt_configs: Dict[str, ProviderConfig] = field(default_factory=dict)
    tts_configs: Dict[str, ProviderConfig] = field(default_factory=dict)
    llm_configs: Dict[str, ProviderConfig] = field(default_factory=dict)
    embedding_configs: Dict[str, ProviderConfig] = field(default_factory=dict)

    @classmethod
    def from_settings(cls) -> "AIConfig":
        """
        Create AIConfig from application settings.
        
        Returns:
            AIConfig instance populated from settings
        """
        config = cls()

        # Load from environment variables or settings
        config.default_stt_provider = getattr(settings, "ai_default_stt_provider", None)
        config.default_tts_provider = getattr(settings, "ai_default_tts_provider", None)
        config.default_llm_provider = getattr(settings, "ai_default_llm_provider", None)
        config.default_embedding_provider = getattr(settings, "ai_default_embedding_provider", None)

        config.global_timeout = getattr(settings, "ai_global_timeout", 30.0)
        config.global_max_retries = getattr(settings, "ai_global_max_retries", 3)
        config.global_retry_delay = getattr(settings, "ai_global_retry_delay", 1.0)
        config.enable_streaming = getattr(settings, "ai_enable_streaming", True)

        # Load provider-specific configurations
        config._load_provider_configs()

        logger.info(
            "AI configuration loaded",
            default_stt=config.default_stt_provider,
            default_tts=config.default_tts_provider,
            default_llm=config.default_llm_provider,
            default_embedding=config.default_embedding_provider,
        )

        return config

    def _load_provider_configs(self) -> None:
        """Load provider-specific configurations from settings."""
        # STT provider configs
        stt_providers = getattr(settings, "ai_stt_providers", {})
        for provider_id, provider_settings in stt_providers.items():
            self.stt_configs[provider_id] = ProviderConfig(
                provider_id=provider_id,
                enabled=provider_settings.get("enabled", True),
                timeout=provider_settings.get("timeout", self.global_timeout),
                max_retries=provider_settings.get("max_retries", self.global_max_retries),
                retry_delay=provider_settings.get("retry_delay", self.global_retry_delay),
                streaming_enabled=provider_settings.get("streaming_enabled", self.enable_streaming),
                custom_settings=provider_settings.get("custom_settings", {}),
            )

        # TTS provider configs
        tts_providers = getattr(settings, "ai_tts_providers", {})
        for provider_id, provider_settings in tts_providers.items():
            self.tts_configs[provider_id] = ProviderConfig(
                provider_id=provider_id,
                enabled=provider_settings.get("enabled", True),
                timeout=provider_settings.get("timeout", self.global_timeout),
                max_retries=provider_settings.get("max_retries", self.global_max_retries),
                retry_delay=provider_settings.get("retry_delay", self.global_retry_delay),
                streaming_enabled=provider_settings.get("streaming_enabled", self.enable_streaming),
                custom_settings=provider_settings.get("custom_settings", {}),
            )

        # LLM provider configs
        llm_providers = getattr(settings, "ai_llm_providers", {})
        for provider_id, provider_settings in llm_providers.items():
            self.llm_configs[provider_id] = ProviderConfig(
                provider_id=provider_id,
                enabled=provider_settings.get("enabled", True),
                timeout=provider_settings.get("timeout", self.global_timeout),
                max_retries=provider_settings.get("max_retries", self.global_max_retries),
                retry_delay=provider_settings.get("retry_delay", self.global_retry_delay),
                streaming_enabled=provider_settings.get("streaming_enabled", self.enable_streaming),
                custom_settings=provider_settings.get("custom_settings", {}),
            )

        # Embedding provider configs
        embedding_providers = getattr(settings, "ai_embedding_providers", {})
        for provider_id, provider_settings in embedding_providers.items():
            self.embedding_configs[provider_id] = ProviderConfig(
                provider_id=provider_id,
                enabled=provider_settings.get("enabled", True),
                timeout=provider_settings.get("timeout", self.global_timeout),
                max_retries=provider_settings.get("max_retries", self.global_max_retries),
                retry_delay=provider_settings.get("retry_delay", self.global_retry_delay),
                streaming_enabled=provider_settings.get("streaming_enabled", self.enable_streaming),
                custom_settings=provider_settings.get("custom_settings", {}),
            )

    def get_stt_config(self, provider_id: str) -> ProviderConfig:
        """
        Get configuration for an STT provider.
        
        Args:
            provider_id: Provider ID
        
        Returns:
            ProviderConfig for the provider
        
        Raises:
            ValueError: If provider not found
        """
        if provider_id not in self.stt_configs:
            # Create default config if not found
            self.stt_configs[provider_id] = ProviderConfig(
                provider_id=provider_id,
                timeout=self.global_timeout,
                max_retries=self.global_max_retries,
                retry_delay=self.global_retry_delay,
                streaming_enabled=self.enable_streaming,
            )
        return self.stt_configs[provider_id]

    def get_tts_config(self, provider_id: str) -> ProviderConfig:
        """
        Get configuration for a TTS provider.
        
        Args:
            provider_id: Provider ID
        
        Returns:
            ProviderConfig for the provider
        
        Raises:
            ValueError: If provider not found
        """
        if provider_id not in self.tts_configs:
            self.tts_configs[provider_id] = ProviderConfig(
                provider_id=provider_id,
                timeout=self.global_timeout,
                max_retries=self.global_max_retries,
                retry_delay=self.global_retry_delay,
                streaming_enabled=self.enable_streaming,
            )
        return self.tts_configs[provider_id]

    def get_llm_config(self, provider_id: str) -> ProviderConfig:
        """
        Get configuration for an LLM provider.
        
        Args:
            provider_id: Provider ID
        
        Returns:
            ProviderConfig for the provider
        
        Raises:
            ValueError: If provider not found
        """
        if provider_id not in self.llm_configs:
            self.llm_configs[provider_id] = ProviderConfig(
                provider_id=provider_id,
                timeout=self.global_timeout,
                max_retries=self.global_max_retries,
                retry_delay=self.global_retry_delay,
                streaming_enabled=self.enable_streaming,
            )
        return self.llm_configs[provider_id]

    def get_embedding_config(self, provider_id: str) -> ProviderConfig:
        """
        Get configuration for an Embedding provider.
        
        Args:
            provider_id: Provider ID
        
        Returns:
            ProviderConfig for the provider
        
        Raises:
            ValueError: If provider not found
        """
        if provider_id not in self.embedding_configs:
            self.embedding_configs[provider_id] = ProviderConfig(
                provider_id=provider_id,
                timeout=self.global_timeout,
                max_retries=self.global_max_retries,
                retry_delay=self.global_retry_delay,
                streaming_enabled=self.enable_streaming,
            )
        return self.embedding_configs[provider_id]

    def set_default_stt(self, provider_id: str) -> None:
        """Set the default STT provider."""
        self.default_stt_provider = provider_id
        logger.info("Default STT provider set", provider_id=provider_id)

    def set_default_tts(self, provider_id: str) -> None:
        """Set the default TTS provider."""
        self.default_tts_provider = provider_id
        logger.info("Default TTS provider set", provider_id=provider_id)

    def set_default_llm(self, provider_id: str) -> None:
        """Set the default LLM provider."""
        self.default_llm_provider = provider_id
        logger.info("Default LLM provider set", provider_id=provider_id)

    def set_default_embedding(self, provider_id: str) -> None:
        """Set the default Embedding provider."""
        self.default_embedding_provider = provider_id
        logger.info("Default Embedding provider set", provider_id=provider_id)


# Global configuration instance
_config: Optional[AIConfig] = None


def get_ai_config() -> AIConfig:
    """
    Get the global AI configuration instance.
    
    Returns:
        AIConfig: The global configuration
    """
    global _config
    if _config is None:
        _config = AIConfig.from_settings()
    return _config
