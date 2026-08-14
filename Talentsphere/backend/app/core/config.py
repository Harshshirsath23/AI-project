from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from sqlalchemy import URL

# Resolve project root directory (e:\Ecosystem\talentsphere)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE_PATH = PROJECT_ROOT / ".env"

class Settings(BaseSettings):
    PROJECT_NAME: str = "TalentSphere AI Enterprise Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security & JWT
    SECRET_KEY: str = Field("talentsphere-super-secret-key-change-in-production-2026", env="SECRET_KEY")
    JWT_SECRET_KEY: str = Field("talentsphere-jwt-secret-key-change-in-production-2026", env="JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 24
    
    # Database Settings
    DB_USER: str = Field("postgres", env="DB_USER")
    DB_PASSWORD: str = Field("admin@123", env="DB_PASSWORD")
    DB_HOST: str = Field("127.0.0.1", env="DB_HOST")
    DB_PORT: int = Field(5433, env="DB_PORT")
    DB_NAME: str = Field("talentsphere", env="DB_NAME")
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000"]
    
    # LangSmith Observability Settings
    LANGSMITH_TRACING: bool = Field(False, validation_alias="LANGSMITH_TRACING")
    LANGSMITH_API_KEY: str | None = Field(None, validation_alias="LANGSMITH_API_KEY")
    LANGSMITH_ENDPOINT: str | None = Field(None, validation_alias="LANGSMITH_ENDPOINT")
    LANGSMITH_PROJECT: str = Field("talentsphere-development", validation_alias="LANGSMITH_PROJECT")
    LANGSMITH_ENVIRONMENT: str = Field("development", validation_alias="LANGSMITH_ENVIRONMENT")
    LANGSMITH_SAMPLING_RATE: float = Field(1.0, validation_alias="LANGSMITH_SAMPLING_RATE")
    LANGSMITH_CAPTURE_INPUTS: bool = Field(False, validation_alias="LANGSMITH_CAPTURE_INPUTS")
    LANGSMITH_CAPTURE_OUTPUTS: bool = Field(False, validation_alias="LANGSMITH_CAPTURE_OUTPUTS")

    # NVIDIA Nemotron 3 Ultra Intelligence Settings
    NEMOTRON_ENABLED: bool = Field(True, validation_alias="NEMOTRON_ENABLED")
    NEMOTRON_MODEL: str = Field("nvidia/nemotron-3-ultra", validation_alias="NEMOTRON_MODEL")
    NEMOTRON_API_KEY: str | None = Field(None, validation_alias="NEMOTRON_API_KEY")
    NEMOTRON_BASE_URL: str = Field("https://integrate.api.nvidia.com/v1", validation_alias="NEMOTRON_BASE_URL")
    NEMOTRON_TIMEOUT_SECONDS: int = Field(30, validation_alias="NEMOTRON_TIMEOUT_SECONDS")
    NEMOTRON_MAX_RETRIES: int = Field(3, validation_alias="NEMOTRON_MAX_RETRIES")
    NEMOTRON_TEMPERATURE: float = Field(0.2, validation_alias="NEMOTRON_TEMPERATURE")
    NEMOTRON_MAX_TOKENS: int = Field(4096, validation_alias="NEMOTRON_MAX_TOKENS")
    NEMOTRON_FALLBACK_ENABLED: bool = Field(True, validation_alias="NEMOTRON_FALLBACK_ENABLED")

    @property
    def is_langsmith_enabled(self) -> bool:
        """Returns True if LangSmith tracing is explicitly enabled and API key is present."""
        return bool(self.LANGSMITH_TRACING and self.LANGSMITH_API_KEY and self.LANGSMITH_API_KEY.strip())
    
    @property
    def host_address(self) -> str:
        return "127.0.0.1" if self.DB_HOST in ["localhost", "::1"] else self.DB_HOST

    @property
    def sync_database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.host_address,
            port=self.DB_PORT,
            database=self.DB_NAME
        )
        
    @property
    def async_database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.host_address,
            port=self.DB_PORT,
            database=self.DB_NAME
        )

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
