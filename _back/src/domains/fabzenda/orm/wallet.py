from sqlalchemy import Column, ForeignKey, Integer, String  # noqa: I001
from sqlalchemy.orm import relationship

from shared.infrastructure.db_base import Base


class WalletORM(Base):
    __tablename__ = "wallet"
    __table_args__ = {"schema": "fabbank"}

    wallet_id = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("public.users.id"), nullable=False)

    def __str__(self) -> str:
        return f"Wallet({self.wallet_id}) - {self.balance} - Owner {self.user}"

    def __repr__(self) -> str:
        return self.__str__()


def setup_relationships():
    from domains.fabbank.orm.transaction import TransactionORM
    from domains.user.orm.user import UserORM

    WalletORM.transactions_from = relationship(
        TransactionORM, foreign_keys=[TransactionORM.wallet_from_id], back_populates="wallet_from"
    )
    WalletORM.transactions_to = relationship(
        TransactionORM, foreign_keys=[TransactionORM.wallet_to_id], back_populates="wallet_to"
    )
    WalletORM.user = relationship(UserORM, foreign_keys=[WalletORM.user_id], back_populates="wallet")


setup_relationships()
