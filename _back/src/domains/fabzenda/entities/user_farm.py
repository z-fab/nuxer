from datetime import datetime

from pydantic import BaseModel

from domains.user.entities.user import UserEntity


class UserFarmEntity(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    user_id: int
    user: UserEntity
    max_animals: int = 3
    created_at: datetime | None = None
    updated_at: datetime | None = None
