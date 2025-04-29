from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from pydantic_core import Url

from domains.user.entities.user import UserEntity


class DebriefingEntity(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    cod: str
    titulo: str
    status: Enum
    url: Url | None

    criado_por: UserEntity | None
    editado_por: UserEntity | None
    criado_em: datetime | None
    editado_em: datetime | None
    enviado_em: datetime | None
    validado_por: UserEntity | None
    validado_em: datetime | None

    produto: list[str]
    solicitante: UserEntity | None
    projeto: list[str]

    estimativa_bi: int
    estimativa_ux: int
    estimativa_writing: int

    descricao: str
    entregaveis: str
    prazo: str
    destaques: str
    limitacoes: str
    premissas: str
    link_workfront: Url | None
    outras_informacoes: str
