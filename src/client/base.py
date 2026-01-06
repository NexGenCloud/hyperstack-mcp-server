"""Base AsyncIO HTTP client implementation."""

import asyncio
import builtins
import json
import types
from typing import Any

import aiohttp
from aioretry import RetryInfo, retry
import structlog

from src.config import settings
from src.exceptions import APIError, RateLimitError, RequestTimeoutError

logger = structlog.get_logger()

# HTTP Status codes
HTTP_NO_CONTENT = 204
HTTP_TOO_MANY_REQUESTS = 429
HTTP_INTERNAL_SERVER_ERROR = 500

# Retry configuration
MAX_RETRY_ATTEMPTS = 3


class BaseAsyncClient:
    """Base async HTTP client with retry and rate limiting support."""

    def __init__(
        self,
        base_url: str,
        headers: dict[str, str] | None = None,
        timeout: int | None = None,
        max_retries: int | None = None,
    ) -> None:
        """Initialize the base client."""
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout or settings.request_timeout
        self.max_retries = max_retries or settings.max_retries
        self._session: aiohttp.ClientSession | None = None
        self._rate_limiter: asyncio.Semaphore | None = None

        # Configure rate limiter if enabled
        if settings.rate_limit_enabled:
            self._rate_limiter = asyncio.Semaphore(settings.rate_limit_requests)

    async def __aenter__(self) -> "BaseAsyncClient":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Async context manager exit."""
        await self.close()

    async def connect(self) -> None:
        """Initialize the HTTP session."""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(
                limit=settings.max_connections,
                limit_per_host=settings.max_keepalive_connections,
                ttl_dns_cache=300,
            )

            timeout_config = aiohttp.ClientTimeout(total=self.timeout)

            self._session = aiohttp.ClientSession(
                connector=connector,
                headers=self.headers,
                timeout=timeout_config,
                json_serialize=lambda obj: json.dumps(obj, default=str),
            )

            logger.info("HTTP session initialized", base_url=self.base_url)

    async def close(self) -> None:
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()
            logger.info("HTTP session closed")

    def _should_retry(self, exception: Exception, attempt: int) -> bool:
        """Determine if request should be retried."""
        if attempt >= self.max_retries:
            return False

        # Retry on specific HTTP errors
        if isinstance(exception, aiohttp.ClientResponseError):
            # Retry on server errors and rate limiting
            return (
                exception.status >= HTTP_INTERNAL_SERVER_ERROR
                or exception.status == HTTP_TOO_MANY_REQUESTS
            )

        # Retry on connection errors
        return isinstance(
            exception,
            aiohttp.ClientConnectorError
            | aiohttp.ServerTimeoutError
            | asyncio.TimeoutError,
        )

    async def _apply_rate_limit(self) -> None:
        """Apply rate limiting if enabled."""
        if self._rate_limiter:
            async with self._rate_limiter:
                # Rate limiter acquired, proceed with request
                await asyncio.sleep(0)  # Yield control

    def _retry_policy(self, info: RetryInfo) -> tuple[bool, float]:
        """Retry policy for HTTP requests."""
        # Check if we should retry based on the exception type
        if info.exception and isinstance(
            info.exception, aiohttp.ClientError | asyncio.TimeoutError
        ):
            # Stop after MAX_RETRY_ATTEMPTS attempts
            if info.fails >= MAX_RETRY_ATTEMPTS:
                return True, 0  # Abandon retry
            # Exponential backoff: 0.5s, 1s, 2s
            delay = 0.5 * (2 ** (info.fails - 1))
            return False, delay  # Continue retrying with delay
        # Don't retry for other exceptions
        return True, 0  # Abandon retry

    @retry("_retry_policy")
    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int | None = None,  # noqa: ASYNC109
    ) -> dict[str, Any]:
        """Execute HTTP request with retry logic."""
        if not self._session:
            await self.connect()

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = {**self.headers, **(headers or {})}
        request_timeout = aiohttp.ClientTimeout(total=timeout or self.timeout)

        # Apply rate limiting
        await self._apply_rate_limit()

        logger.debug(
            "Making HTTP request",
            method=method,
            url=url,
            params=params,
            has_body=json_data is not None,
        )

        try:
            async with self._session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=request_headers,
                timeout=request_timeout,
            ) as response:
                response_data = await self._handle_response(response)

                logger.debug(
                    "Request successful",
                    method=method,
                    url=url,
                    status=response.status,
                )

                return response_data

        except builtins.TimeoutError as e:
            logger.exception("Request timeout", url=url, timeout=request_timeout.total)
            raise RequestTimeoutError(
                f"Request to {url} timed out after {request_timeout.total}s"
            ) from e

        except aiohttp.ClientResponseError as e:
            if e.status == HTTP_TOO_MANY_REQUESTS:
                logger.warning("Rate limit exceeded", url=url)
                raise RateLimitError(
                    "Rate limit exceeded",
                    status_code=e.status,
                    response_body=str(e),
                ) from e

            logger.exception(
                "HTTP error",
                url=url,
                status=e.status,
                message=str(e),
            )

            raise APIError(
                f"HTTP {e.status}: {e.message}",
                status_code=e.status,
                response_body=str(e),
            ) from e

        except aiohttp.ClientError as e:
            logger.exception("Client error", url=url, error=str(e))
            raise APIError(f"Client error: {e!s}") from e

    async def _handle_response(
        self, response: aiohttp.ClientResponse
    ) -> dict[str, Any]:
        """Handle HTTP response."""
        response.raise_for_status()

        # Handle empty responses
        if response.status == HTTP_NO_CONTENT:
            return {}

        # Parse JSON response
        try:
            return await response.json()
        except (json.JSONDecodeError, aiohttp.ContentTypeError) as e:
            # Try to get text response for debugging
            text = await response.text()
            logger.exception(
                "Failed to parse response",
                status=response.status,
                content_type=response.headers.get("Content-Type"),
                body_preview=text[:200] if text else None,
            )
            raise APIError(
                f"Invalid response format: {e!s}",
                status_code=response.status,
                response_body=text,
            ) from e

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute GET request."""
        return await self.request("GET", endpoint, params=params, **kwargs)

    async def post(
        self,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute POST request."""
        return await self.request("POST", endpoint, json_data=json_data, **kwargs)

    async def put(
        self,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute PUT request."""
        return await self.request("PUT", endpoint, json_data=json_data, **kwargs)

    async def patch(
        self,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute PATCH request."""
        return await self.request("PATCH", endpoint, json_data=json_data, **kwargs)

    async def delete(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute DELETE request."""
        return await self.request("DELETE", endpoint, **kwargs)
