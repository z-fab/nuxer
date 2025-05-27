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
            "REWARD": "- Aumenta em %x o valor de sorteio dos seus Fabichinhos",
        }

        if self.effect_type == "STATE_CHANGE":
            for item_def in self.effect:
                if item_def in mapping:
                    text += mapping[item_def] + "\n"
        else:
            for item_def in self.effect:
                if item_def in mapping:
                    value_multiplier = (self.effect[item_def] - 1) * 100
                    text += mapping[item_def].replace("%x", f"{value_multiplier:.0f}%") + "\n"

        return text.strip()
