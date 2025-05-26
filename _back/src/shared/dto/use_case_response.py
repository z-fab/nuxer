from pydantic import BaseModel, Field

from shared.dto.error_code import ErrorCode
from shared.dto.use_case_request import UseCaseCode


class UseCaseResponse(BaseModel):
    success: bool
    code: UseCaseCode
    error_code: ErrorCode = None
    data: dict | None = Field(default_factory=dict)
