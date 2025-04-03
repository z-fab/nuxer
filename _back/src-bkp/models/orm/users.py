from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
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

    wallet = relationship("Wallet", back_populates="user", uselist=False)
    animals = relationship("UserAnimal", back_populates="user", uselist=False)

    def __str__(self) -> str:
        return f"User(Nome: {self.nome} ({self.id})"

    def __repr__(self) -> str:
        return f"User(Nome: {self.nome} ({self.id})"
