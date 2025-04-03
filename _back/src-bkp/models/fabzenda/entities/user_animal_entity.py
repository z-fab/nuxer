from datetime import datetime

from pydantic import BaseModel, Field

from models.entities.user_entity import UserEntity
from models.fabzenda.entities.animal_modifier_entity import AnimalModifierEntity
from models.fabzenda.entities.animal_type_entity import AnimalTypeEntity


class UserAnimalEntity(BaseModel):
    animal_id: int = Field(..., description="ID do animal")
    user_id: int = Field(..., description="ID do usuário")
    user_entity: UserEntity | None = Field(None, description="Entidade do USer")
    type_id: int = Field(..., description="ID do tipo")
    animal_type: AnimalTypeEntity | None = Field(None, description="Entidade do Animal")
    name: str = Field(..., min_length=1, max_length=50, description="Nome do animal")
    purchase_date: datetime = Field(..., description="Data de compra do animal")
    last_fed: datetime = Field(..., description="Data da última alimentação do animal")
    food_slot: int = Field(..., description="Slots de comida disponíveis")
    health: int = Field(..., description="Saúde do animal")
    health_str: str = Field(..., description="Saúde do animal em texto")
    expiry_date: datetime = Field(..., description="Data de expiração do animal")
    is_alive: bool = Field(..., description="Se o animal está vivo")
    modifier_id: int | None = Field(None, description="ID do modificador")
    modifier: AnimalModifierEntity | None = Field(None, description="Entidade do Modificador")
