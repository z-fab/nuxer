from pydantic import BaseModel


class AnimalTypeEntity(BaseModel):
    model_config = {"from_attributes": True}

    type_id: int
    name: str
    emoji: str
    base_price: int
    base_reward: int
    hunger_rate: int
    lifespan: int
    available: bool
    description: str
