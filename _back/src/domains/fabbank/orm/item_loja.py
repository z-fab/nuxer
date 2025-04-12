from sqlalchemy import Boolean, Column, Integer, String

from shared.infrastructure.db_base import Base


class ItemLojaORM(Base):
    __tablename__ = "itens_loja"
    __table_args__ = {"schema": "fabbank"}

    cod = Column(String, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=True)
    descricao = Column(String, nullable=True)
    valor = Column(Integer, nullable=False)
    valor_real = Column(Boolean, nullable=True)
    amount = Column(Integer, nullable=False)
    enable = Column(Boolean, nullable=False)

    def __str__(self) -> str:
        return f"ItemLoja({self.cod}) - {self.nome} - {self.valor} - {self.valor_real} - {self.amount} - {self.enable})"

    def __repr__(self) -> str:
        return self.__str__()
