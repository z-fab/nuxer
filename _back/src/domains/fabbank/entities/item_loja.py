from pydantic import BaseModel


class ItemLojaEntity(BaseModel):
    model_config = {"from_attributes": True}

    cod: str
    nome: str
    descricao: str
    valor: int
    valor_real: bool
    amount: int
    enable: bool
