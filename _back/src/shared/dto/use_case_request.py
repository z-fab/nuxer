from pydantic import BaseModel

from shared.dto.use_case_code import UseCaseCode


class UseCaseRequest(BaseModel):
    source: str
    code: UseCaseCode
    payload: dict | None = None
