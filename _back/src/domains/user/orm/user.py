from sqlalchemy import Boolean, Column, Integer, String  # noqa: I001
from sqlalchemy.orm import relationship

from shared.infrastructure.db_base import Base


class UserORM(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id: str = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String, nullable=False)
    slack_id: str = Column(String, nullable=False)
    notion_id: str = Column(String, nullable=False)
    notion_user_id: str = Column(String, nullable=True)
    apelido: str = Column(String, nullable=True)
    email: str = Column(String, nullable=True)
    ativo: str = Column(Boolean, nullable=False)
    role: int = Column(Integer, nullable=False)

    def __str__(self) -> str:
        return f"User(Nome: {self.nome} ({self.id})"

    def __repr__(self) -> str:
        return f"User(Nome: {self.nome} ({self.id})"


def setup_relationships():
    from domains.fabbank.orm.wallet import WalletORM
    from domains.fabzenda.orm.user_animal import UserAnimalORM

    UserORM.wallet = relationship(WalletORM, back_populates="user", uselist=False)
    UserORM.animals = relationship(UserAnimalORM, back_populates="user", uselist=False)


setup_relationships()
