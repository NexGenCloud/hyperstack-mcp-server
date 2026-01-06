from typing import Any

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    success: bool = False
    status: str | None = None
    message: str | None = None
    code: Any | None = None
    details: Any | None = None
