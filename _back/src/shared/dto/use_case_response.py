from pydantic import BaseModel, Field


class UseCaseResponse(BaseModel):
    success: bool
    message: str | None = None
    data: dict | None = Field(default_factory=dict)
    notification: list[dict] | None = None
