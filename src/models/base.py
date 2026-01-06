"""Base Pydantic models for Hyperstack resources."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BaseResource(BaseModel):
    """Base model for all Hyperstack resources."""

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    id: int = Field(..., description="Resource ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime | None = Field(None, description="Last update timestamp")


class PaginationParams(BaseModel):
    """Pagination parameters."""

    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel):
    """Paginated response model."""

    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    count: int = Field(..., description="Total number of items")
    results: list[Any] = Field(default_factory=list, description="Result items")
    next: str | None = Field(None, description="Next page URL")
    previous: str | None = Field(None, description="Previous page URL")


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error message")
    code: str | None = Field(None, description="Error code")
    details: dict[str, Any] | None = Field(None, description="Error details")


class SuccessResponse(BaseModel):
    """Success response model."""

    success: bool = Field(default=True, description="Success indicator")
    message: str | None = Field(None, description="Success message")
    data: dict[str, Any] | None = Field(None, description="Response data")
