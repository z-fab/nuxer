from datetime import datetime

from pydantic import BaseModel

from domains.fabzenda.entities.animal_modifier import AnimalModifierEntity
from domains.fabzenda.entities.animal_type import AnimalTypeEntity
from domains.user.entities.user import UserEntity


class UserAnimalEntity(BaseModel):
    model_config = {"from_attributes": True}

    animal_id: int
    user_id: int
    user: UserEntity | None = None
    type_id: int
    animal_type: AnimalTypeEntity
    name: str
    purchase_date: datetime
    last_fed: datetime
    food_slot: int
    health: int
    expiry_date: datetime
    is_alive: bool
    modifier_id: int | None
    modifier: AnimalModifierEntity | None = None

    @property
    def hunger_rate(self) -> int:
        base = self.animal_type.hunger_rate if self.animal_type else 24
        if self.modifier:
            return round(base * self.modifier.hunger_rate_multiplier)
        return base

    @property
    def lifespan(self) -> int:
        base = self.animal_type.lifespan if self.animal_type else 14
        if self.modifier:
            return max(1, round(base * self.modifier.lifespan_multiplier))
        return base

    @property
    def feeding_cost(self) -> int:
        base = 2
        if self.modifier:
            return max(1, round(base * self.modifier.feeding_cost_multiplier))
        return base

    @property
    def burial_cost(self) -> int:
        base = 1
        if self.modifier:
            return max(0, round(base * self.modifier.burial_cost_multiplier))
        return base

    @property
    def expire_value(self) -> int:
        if not self.animal_type:
            return 0
        base = round(self.animal_type.base_price * 0.25)
        if self.modifier:
            return max(0, round(base * self.modifier.expire_multiplier))
        return base

    @property
    def found_coin_percentage(self) -> float:
        return self.modifier.found_coin_percentage if self.modifier else 0.05

    @property
    def reward(self) -> int:
        base = self.animal_type.base_reward if self.animal_type else 0

        # Aplica o modificador
        if self.modifier:
            base = round(base * self.modifier.reward_multiplier)

        # Aplica o modificador de health
        match self.health:
            case 3:
                base *= 0.75
            case 2:
                base *= 0.5
            case 1:
                base *= 0.1
            case 0 | -1:
                return 0

        return round(base)

    @property
    def health_str(self) -> str:
        mapping = {
            4: "Saudável 🥰",
            3: "Faminto 🫠",
            2: "Desnutrido 😞",
            1: "Doente 😵‍💫",
            0: "Morto 💀",
        }
        return mapping.get(self.health, "Desconhecido ❓")
