from datetime import datetime

from pydantic import BaseModel

from domains.user.entities.user import UserEntity


class WalletEntity(BaseModel):
    model_config = {"from_attributes": True}

    wallet_id: str
    user_id: int
    user: UserEntity | None = None
    balance: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
