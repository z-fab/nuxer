from pydantic import BaseModel


class UserEntity(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    nome: str
    apelido: str
    email: str | None = None
    slack_id: str
    notion_id: str | None = None
    notion_user_id: str | None = None
    ativo: bool
    role: int
