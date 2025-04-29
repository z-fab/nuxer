from pydantic import BaseModel, EmailStr


class MagicLinkRequestEntity(BaseModel):
    email: EmailStr
