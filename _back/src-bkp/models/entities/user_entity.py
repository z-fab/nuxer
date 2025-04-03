from pydantic import BaseModel


class UserEntity(BaseModel):
    id: int = None
    nome: str = None
    apelido: str = None
    email: str | None = None
    slack_id: str = None
    notion_id: str | None = None
    notion_user_id: str | None = None
    ativo: bool = None
    role: int = None
