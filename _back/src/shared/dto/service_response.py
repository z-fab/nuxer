from enum import Enum

from pydantic import BaseModel


class ServiceResponse(BaseModel):
    success: bool
    error: str | Enum | None = None
    data: dict | None = None
