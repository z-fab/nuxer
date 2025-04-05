from pydantic import BaseModel


class UseCaseResponse(BaseModel):
    success: bool
    message: str | None = None
    data: dict | None = {}
    notification: list[dict] | None
