from pydantic import BaseModel, Field


class AnimalModifierEntity(BaseModel):
    modifier_id: int = Field(..., description="ID do modificador")
    name: str = Field(..., min_length=1, max_length=50, description="Nome do modificador")
    emoji: str = Field(..., min_length=1, max_length=5, description="Emoji do modificador")
    description: str | None = Field(None, description="Descrição do modificador")
    rarity: int = Field(..., description="Raridade do modificador (0=comum, 1=incomum, 2=raro)")
    rarity_str: str = Field(..., description="Raridade do modificador em texto")
    feeding_cost_multiplier: float = Field(1.0, description="Multiplicador do custo de alimentação")
    burial_cost_multiplier: float = Field(1.0, description="Multiplicador do custo de enterro")
    hunger_rate_multiplier: float = Field(1.0, description="Multiplicador da taxa de fome")
    expire_multiplier: float = Field(1.0, description="Multiplicador do valor ao expirar")
    reward_multiplier: float = Field(1.0, description="Multiplicador da recompensa")
    lifespan_multiplier: float = Field(1.0, description="Multiplicador do tempo de vida")
    found_coin_percentage: float = Field(5.0, description="Porcentagem de chance de encontrar moeda")

    # Campos calculados para exibição
    resume_modifier: str = Field(..., description="Texto resumido do modificador")
    feeding_cost_text: str = Field(..., description="Texto do custo de alimentação")
    burial_cost_text: str = Field(..., description="Texto do custo de enterro")
    hunger_rate_text: str = Field(..., description="Texto da taxa de fome")
    expire_value_text: str = Field(..., description="Texto do valor ao expirar")
    reward_text: str = Field(..., description="Texto da recompensa")
    lifespan_text: str = Field(..., description="Texto do tempo de vida")
    found_coin_text: str = Field(..., description="Texto da chance de encontrar moeda")
