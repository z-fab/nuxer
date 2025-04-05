from pydantic import BaseModel


class ServiceResponse(BaseModel):
    success: bool
    error: str | None = None
    data: dict | None = None
