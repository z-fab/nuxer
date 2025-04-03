from datetime import datetime
from pydantic import BaseModel

from models.entities.user_entity import UserEntity

class EchoEntity(BaseModel):

    cod: int = None
    situacao: str = None
    titulo: str = None
    descricao: str = None
    file_url: str = None
    tags: list[str] = None
    criado_em: datetime | None = None
    criado_por: UserEntity | None = None