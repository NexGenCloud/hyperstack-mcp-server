"""Custom exceptions for Hyperstack MCP Server."""

from typing import Any


class HyperstackMCPError(Exception):
    """Base exception for Hyperstack MCP Server."""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize exception."""
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class ConfigurationError(HyperstackMCPError):
    """Configuration related errors."""


class AuthenticationError(HyperstackMCPError):
    """Authentication related errors."""


class APIError(HyperstackMCPError):
    """API communication errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize API error."""
        super().__init__(message, **kwargs)
        self.status_code = status_code
        self.response_body = response_body


class RateLimitError(APIError):
    """Rate limiting errors."""


class ValidationError(HyperstackMCPError):
    """Data validation errors."""


class ResourceNotFoundError(HyperstackMCPError):
    """Resource not found errors."""


class ResourceConflictError(HyperstackMCPError):
    """Resource conflict errors."""


class RequestTimeoutError(HyperstackMCPError):
    """Timeout errors."""


class RetryExhaustedError(HyperstackMCPError):
    """Retry attempts exhausted."""

    def __init__(
        self,
        message: str,
        attempts: int,
        last_error: Exception | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize retry exhausted error."""
        super().__init__(message, **kwargs)
        self.attempts = attempts
        self.last_error = last_error
