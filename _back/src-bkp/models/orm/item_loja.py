from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class ItemLoja(Base):
    __tablename__ = "itens_loja"
    __table_args__ = {"schema": "fabbank"}

    cod: str = Column(String, primary_key=True, autoincrement=True)
    nome: str = Column(String, nullable=True)
    descricao: str = Column(String, nullable=True)
    valor: str = Column(Integer, nullable=False)
    valor_real: str = Column(Boolean, nullable=True)
    amount: str = Column(Integer, nullable=False)
    enable: bool = Column(Boolean, nullable=False)

    def __str__(self) -> str:
        return f"[ItemLoja] {self.nome} ({self.cod}) - {self.descricao} :: Valor: {self.valor} :: Quantidade: {self.amount}"  # noqa: E501

    def __repr__(self) -> str:
        return f"[ItemLoja] {self.nome} ({self.cod}) - {self.descricao} :: Valor: {self.valor} :: Quantidade: {self.amount}"  # noqa: E501
