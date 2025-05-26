from pydantic import BaseModel

from shared.dto.error_code import ErrorCode


class ServiceResponse(BaseModel):
    success: bool
    error: ErrorCode = None
    data: dict | None = None
