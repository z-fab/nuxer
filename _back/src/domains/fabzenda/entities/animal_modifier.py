from pydantic import BaseModel


class AnimalModifierEntity(BaseModel):
    model_config = {"from_attributes": True}

    modifier_id: int
    name: str
    emoji: str
    description: str
    rarity: int
    feeding_cost_multiplier: float
    burial_cost_multiplier: float
    hunger_rate_multiplier: float
    expire_multiplier: float
    reward_multiplier: float
    lifespan_multiplier: float
    found_coin_percentage: float

    @property
    def rarity_str(self) -> str:
        return {0: "Comum", 1: "Incomum", 2: "Raro"}.get(self.rarity, "Desconhecido")

    @property
    def feeding_cost_text(self) -> str:
        return self._get_multiplier_text(
            self.feeding_cost_multiplier, "A comida custará", "menos fabcoins", "mais fabcoins"
        )

    @property
    def burial_cost_text(self) -> str:
        return self._get_multiplier_text(
            self.burial_cost_multiplier, "O enterro custará", "menos fabcoins", "mais fabcoins"
        )

    @property
    def hunger_rate_text(self) -> str:
        return self._get_multiplier_text(self.hunger_rate_multiplier, "O tempo de alimentação será", "menor", "maior")

    @property
    def expire_value_text(self) -> str:
        return self._get_multiplier_text(
            self.expire_multiplier, "Ao ser abduzido, você receberá", "menos fabcoins", "mais fabcoins"
        )

    @property
    def reward_text(self) -> str:
        return self._get_multiplier_text(
            self.reward_multiplier, "Quando sorteado, você receberá", "menos fabcoins", "mais fabcoins"
        )

    @property
    def lifespan_text(self) -> str:
        return self._get_multiplier_text(self.lifespan_multiplier, "O fabichinho viverá", "menos tempo", "mais tempo")

    @property
    def found_coin_text(self) -> str:
        if self.found_coin_percentage == 0:
            return "Não *encontra fabcoins* diariamente"
        elif self.found_coin_percentage > 0.05:
            return "Tem *mais chance* de encontrar fabcoins diariamente"
        elif self.found_coin_percentage < 0.05:
            return "Tem *menos chance* de encontrar fabcoins diariamente"
        return ""

    @property
    def resume_modifier(self) -> str:
        items = [
            self.feeding_cost_text,
            self.burial_cost_text,
            self.hunger_rate_text,
            self.expire_value_text,
            self.reward_text,
            self.lifespan_text,
            self.found_coin_text,
        ]
        items = [txt for txt in items if txt]
        if not items:
            return "Esse modificador não altera o comportamento do fabichinho."
        if len(items) == 1:
            return f"Por causa do modificador: {items[0]}."
        return f"Por causa do modificador: {'; '.join(items[:-1])} e {items[-1]}."

    def _get_multiplier_text(self, multiplier: float, phrase: str, complement_pos: str, complement_neg: str) -> str:
        if multiplier == 1.0:
            return ""
        change = abs((multiplier - 1.0) * 100)
        if multiplier < 1.0:
            return f"{phrase} *{change:.0f}% {complement_pos}*"
        else:
            return f"{phrase} *{change:.0f}% {complement_neg}*"
