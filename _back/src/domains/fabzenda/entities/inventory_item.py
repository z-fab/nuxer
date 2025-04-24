from datetime import datetime

from pydantic import BaseModel

from domains.fabzenda.entities.item_definition import ItemDefinitionEntity
from domains.fabzenda.entities.user_animal import UserAnimalEntity
from domains.user.entities.user import UserEntity


class InventoryItemEntity(BaseModel):
    model_config = {"from_attributes": True}

    inventory_id: int
    item_id: int
    item_definition: ItemDefinitionEntity
    user_id: int
    user: UserEntity
    user_animal_id: int | None = None
    user_animal: UserAnimalEntity | None = None
    quantity: int
    equipped_at: datetime
    expired_at: datetime | None = None
