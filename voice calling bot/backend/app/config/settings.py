from functools import lru_cache
from typing import List, Dict, Any
from urllib.parse import quote_plus

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration using Pydantic settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="Enterprise AI Calling Platform", description="Application name")
    app_env: str = Field(default="development", description="Environment (development/staging/production)")
    app_debug: bool = Field(default=True, description="Debug mode")
    app_version: str = Field(default="0.1.0", description="Application version")
    api_prefix: str = Field(default="/api/v1", description="API prefix")

    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    workers: int = Field(default=4, description="Number of worker processes")

    # Database
    db_host: str = Field(default="localhost", description="Database host")
    db_port: int = Field(default=5432, description="Database port")
    db_user: str = Field(default="user", description="Database user")
    db_password: str = Field(default="password", description="Database password")
    db_name: str = Field(default="ai_calling_platform", description="Database name")
    database_pool_size: int = Field(default=20, description="Database pool size")
    database_max_overflow: int = Field(default=10, description="Database max overflow")
    database_echo: bool = Field(default=False, description="Database query echo")

    @property
    def database_url(self) -> str:
        """Construct database URL from individual components."""
        # Use 127.0.0.1 instead of localhost to avoid DNS resolution issues
        host = "127.0.0.1" if self.db_host == "localhost" else self.db_host
        # URL-encode password to handle special characters like @
        encoded_password = quote_plus(self.db_password)
        return f"postgresql+asyncpg://{self.db_user}:{encoded_password}@{host}:{self.db_port}/{self.db_name}"

    @property
    def sync_database_url(self) -> str:
        """Construct synchronous database URL for Alembic migrations."""
        # Use 127.0.0.1 instead of localhost to avoid DNS resolution issues
        host = "127.0.0.1" if self.db_host == "localhost" else self.db_host
        # URL-encode password to handle special characters like @
        encoded_password = quote_plus(self.db_password)
        return f"postgresql+psycopg://{self.db_user}:{encoded_password}@{host}:{self.db_port}/{self.db_name}"

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", description="Redis connection URL")
    redis_max_connections: int = Field(default=20, description="Redis max connections")

    # Celery
    celery_broker_url: str = Field(default="redis://localhost:6379/1", description="Celery broker URL")
    celery_result_backend: str = Field(default="redis://localhost:6379/2", description="Celery result backend")

    # Security
    secret_key: str = Field(default="your-secret-key-change-in-production", description="Secret key for JWT")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="Access token expiration in minutes")

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        description="CORS allowed origins",
    )

    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="json", description="Log format (json/text)")

    # AI Providers
    gemini_api_key: str = Field(default="", description="Gemini API key")
    sarvam_api_key: str = Field(default="", description="Sarvam API key")
    nvidia_api_key: str = Field(default="", description="NVIDIA API key")
    huggingface_api_key: str = Field(default="", description="Hugging Face API token")


    # AI Configuration
    ai_default_stt_provider: str = Field(default="faster_whisper", description="Default STT provider")
    ai_default_tts_provider: str = Field(default="piper", description="Default TTS provider")
    ai_default_llm_provider: str = Field(default="gemini", description="Default LLM provider")
    ai_default_embedding_provider: str = Field(default="sentence_transformers", description="Default Embedding provider")
    ai_global_timeout: float = Field(default=30.0, description="Global AI operation timeout in seconds")
    ai_global_max_retries: int = Field(default=3, description="Global max retries for AI operations")
    ai_global_retry_delay: float = Field(default=1.0, description="Global retry delay in seconds")
    ai_enable_streaming: bool = Field(default=True, description="Enable streaming for AI operations")

    # Telephony
    twilio_account_sid: str = Field(default="", description="Twilio account SID")
    twilio_auth_token: str = Field(default="", description="Twilio auth token")
    twilio_phone_number: str = Field(default="", description="Twilio phone number")
    # Public base URL for Twilio webhooks.
    # When testing locally, set this to your localtunnel URL e.g. https://xxxx.loca.lt
    webhook_base_url: str = Field(default="http://localhost:8000", description="Public base URL for Twilio webhooks")


    # Conversation Configuration
    conversation_session_timeout: int = Field(default=300, description="Conversation session timeout in seconds")
    conversation_max_length: int = Field(default=1000, description="Maximum conversation length in turns")
    conversation_idle_time: int = Field(default=60, description="Conversation idle time in seconds")
    conversation_memory_limit: int = Field(default=10000, description="Conversation memory limit in characters")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.app_env == "development"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
