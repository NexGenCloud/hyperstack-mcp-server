"""Configuration management for Hyperstack MCP Server."""

from enum import StrEnum

from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(StrEnum):
    """Environment enum."""

    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra environment variables
    )

    environment: Env = Field(
        default=Env.LOCAL, description="Application environment (dev, prod, local)"
    )

    # API Configuration
    hyperstack_api_key: str = Field(
        ..., description="Hyperstack API key for authentication"
    )
    hyperstack_api_url: HttpUrl = Field(
        default="https://infrahub-api.nexgencloud.com/v1",
        description="Hyperstack API base URL",
    )

    # Logging Configuration
    log_level: str = Field(
        default="INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    log_format: str = Field(default="json", description="Log format (json or text)")

    # Connection Pool Configuration
    max_connections: int = Field(
        default=100, description="Maximum number of connections in the pool"
    )
    max_keepalive_connections: int = Field(
        default=50, description="Maximum number of keepalive connections"
    )
    keepalive_expiry: int = Field(
        default=5, description="Keepalive expiry time in seconds"
    )

    # Request Configuration
    request_timeout: int = Field(
        default=30, description="Default request timeout in seconds"
    )
    max_retries: int = Field(default=3, description="Maximum number of retry attempts")
    retry_backoff_factor: float = Field(
        default=2.0, description="Exponential backoff factor for retries"
    )

    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_requests: int = Field(
        default=100, description="Maximum requests per minute"
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"Invalid log level. Must be one of: {valid_levels}")
        return v

    @field_validator("hyperstack_api_url")
    @classmethod
    def validate_api_url(cls, v: HttpUrl) -> HttpUrl:
        """Ensure API URL doesn't have trailing slash."""
        url_str = str(v)
        if url_str.endswith("/"):
            return HttpUrl(url_str[:-1])
        return v

    @field_validator("environment", mode="before")
    @classmethod
    def normalize_env(cls, v: str | Env | None) -> str | Env:
        if isinstance(v, str):
            return v.lower()
        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == Env.LOCAL

    def get_auth_headers(self) -> dict[str, str]:
        """Get authentication headers for API requests."""
        return {
            "Accept": "application/json",
            "api-key": self.hyperstack_api_key,
        }


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()


# Global settings instance
settings = get_settings()
