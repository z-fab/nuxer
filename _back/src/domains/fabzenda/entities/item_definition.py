from datetime import datetime

from pydantic import BaseModel


class ItemDefinitionEntity(BaseModel):
    model_config = {"from_attributes": True}

    item_id: int
    name: str
    emoji: str
    price: int
    description: str
    item_target: str
    effect_type: str
    effect: dict
    duration: datetime | None
    available: bool

    @property
    def effect_str(self) -> str:
        text = ""
        mapping = {
            "ADD_SLOT_FARM": "- Adiciona mais %x espaço de Fabichinho na sua Fabzenda",
            "REWARD_MULT": "- Aumenta em %x o valor de sorteio dos seu Fabichinho",
            "CHANGE_MODIFIER": "- Altera o modificador do Fabichinho para %x",
            "ADD_EXPIRE_DAY": "- Aumenta em %x dias o tempo de vida dos seu Fabichinho",
            "ADD_HUNGER_DAY": "- Faz seu Fabichinho não sentir fome por %x dias",
        }

        for item_def in self.effect:
            if item_def in mapping:
                value_multiplier = (self.effect[item_def] - 1) * 100
                text += mapping[item_def].replace("%x", f"{value_multiplier:.0f}%") + "\n"

        return text.strip()
