from datetime import datetime

from pydantic import BaseModel


class ItemDefinitionEntity(BaseModel):
    model_config = {"from_attributes": True}

    item_id: int
    name: str
    emoji: str
    price: int
    description: str
    effect_type: str
    effect: dict
    duration: datetime | None
    available: bool

    @property
    def effect_str(self) -> str:
        text = ""
        mapping = {
            "ADD_SLOT_FARM": "- Adiciona mais um espaço de Fabichinho na sua Fabzenda",
        }

        for item_def in self.effect:
            if item_def in mapping:
                text += mapping[item_def] + "\n"

        return text.strip()
