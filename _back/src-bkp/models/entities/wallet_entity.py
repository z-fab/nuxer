from typing import Optional
from pydantic import BaseModel

from models.entities.user_entity import UserEntity


class WalletEntity(BaseModel):
    wallet_id: str = None
    balance: int = None
    user: UserEntity = None
