from pydantic import BaseModel

class ItemLojaEntity(BaseModel):
    cod: str = None
    nome: str = None
    descricao: str = None
    valor: int = 1
    valor_real: int = 1
    amount: int = -1
    enable: bool = True
