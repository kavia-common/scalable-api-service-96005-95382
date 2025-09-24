import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # Service
    APP_ENV: str = Field(default="development", description="Application environment (development/staging/production)")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    CORS_ALLOW_ORIGINS: list[str] = Field(default_factory=lambda: ["*"], description="CORS allowed origins")

    # Security for FastAPI endpoints
    API_BEARER_TOKEN: str = Field(default="", description="Static bearer token to protect API endpoints")

    # Grafana integration
    GRAFANA_URL: AnyHttpUrl = Field(default="http://localhost:3000", description="Base URL for Grafana")
    GRAFANA_API_KEY: str = Field(default="", description="Grafana API Key used for outgoing requests")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def is_auth_enabled(self) -> bool:
        """
        Whether API auth is enabled. If API_BEARER_TOKEN is set, auth is enabled.
        """
        return bool(self.API_BEARER_TOKEN)


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Expose singleton settings
settings = get_settings()
