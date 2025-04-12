from sqlalchemy import Column, Integer, String  # noqa: I001

from shared.infrastructure.db_base import Base


class ConfigORM(Base):
    __tablename__ = "config"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)

    def __str__(self) -> str:
        return f"Wallet({self.wallet_id}) - {self.balance} - Owner {self.user}"

    def __repr__(self) -> str:
        return self.__str__()
