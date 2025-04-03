import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class MagicLinkRequest(BaseModel):
    email: EmailStr


# class APIKey(BaseModel):
#     id: int
#     key: str
#     name: str
#     created_at: datetime
#     user_id: int
