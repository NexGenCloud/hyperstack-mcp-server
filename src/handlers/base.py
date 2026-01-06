"""Base handler class for MCP actions."""

from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError
import structlog

from src.client.hyperstack import get_client
from src.exceptions import HyperstackMCPError
from src.models.errors import ErrorSchema

logger = structlog.get_logger()

T = TypeVar("T")


class BaseHandler:
    """Base handler with common functionality."""

    def __init__(self) -> None:
        """Initialize base handler."""
        self.client = get_client()
        self.logger = structlog.get_logger(self.__class__.__name__)

    async def validate_response(
        self, response: dict[str, Any], operation: str, response_schema: BaseModel
    ) -> dict[str, Any]:
        """Validate API response."""
        if not response:
            raise HyperstackMCPError(
                f"Empty response from {operation}",
                code="EMPTY_RESPONSE",
            )

        # Check for error responses
        if "error" in response:
            raise HyperstackMCPError(
                response.get("error", "Unknown error"),
                code=response.get("error_code", "API_ERROR"),
                details=response,
            )

        # check for status
        if response.get("status") is False:
            raise HyperstackMCPError(
                response.get("message", "Unknown error"),
                code=response.get("error_code", "API_ERROR"),
                details=response,
            )

        try:
            response_schema(**response)
        except ValidationError as e:
            raise HyperstackMCPError(
                "Invalid response", code="VALIDATION_ERROR", details=e.errors()
            ) from e

        return response

    def format_success_response(
        self,
        message: str,
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Format a successful response."""
        response = {
            "success": True,
            "message": message,
        }

        if data is not None:
            response["data"] = data

        # Add any additional fields
        response.update(kwargs)

        return response

    def format_list_response(
        self,
        items: list[Any],
        total: int | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        """Format a list response."""
        response = {
            "success": True,
            "count": len(items),
            "results": items,
        }

        if total is not None:
            response["total"] = total
        if page is not None:
            response["page"] = page
        if page_size is not None:
            response["page_size"] = page_size

        return response

    def format_error_response(
        self,
        err: HyperstackMCPError,
        code: str,
    ) -> ErrorSchema:
        """Format an error response."""
        return ErrorSchema(
            status="error",
            message=err.message,
            code=code,
            details=err.details,
        )
