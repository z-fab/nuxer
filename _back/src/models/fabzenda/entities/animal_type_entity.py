from pydantic import BaseModel, Field


class AnimalTypeEntity(BaseModel):
    type_id: int = Field(..., description="ID do tipo")
    name: str = Field(..., min_length=1, max_length=50, description="Nome do animal")
    emoji: str = Field(..., min_length=1, max_length=10, description="Emoji representativo do animal")
    base_price: int = Field(..., gt=0, description="Preço base em Fabcoins para compra do animal")
    base_reward: int = Field(..., gt=0, description="Recompensa base em Fabcoins quando o animal é sorteado")
    hunger_rate: int = Field(
        ..., gt=0, description="Taxa de fome em horas (quanto tempo leva para perder slots de fome)"
    )
    lifespan: int = Field(..., gt=0, description="Tempo de vida em dias")
    available: bool = Field(True, description="Se o animal está disponível para compra")
    description: str | None = Field(None, description="Descrição detalhada do animal")
