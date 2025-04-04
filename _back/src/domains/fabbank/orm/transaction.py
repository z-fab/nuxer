from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String  # noqa: I001
from sqlalchemy.orm import relationship

from shared.infrastructure.db_base import Base


class TransactionORM(Base):
    __tablename__ = "transaction"
    __table_args__ = {"schema": "fabbank"}

    transaction_id = Column(String, primary_key=True)
    wallet_from_id = Column(String, ForeignKey("fabbank.wallet.wallet_id"), nullable=False)
    wallet_to_id = Column(String, ForeignKey("fabbank.wallet.wallet_id"), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.now)

    def __str__(self) -> str:
        return f"Transaction({self.transaction_id}) - {self.amount} - From {self.wallet_from_id} to {self.wallet_to_id}"

    def __repr__(self) -> str:
        return self.__str__()


def setup_relationships():
    TransactionORM.wallet_from = relationship(
        "WalletORM",
        primaryjoin="TransactionORM.wallet_from_id==WalletORM.wallet_id",
        back_populates="transactions_from",
    )
    TransactionORM.wallet_to = relationship(
        "WalletORM", primaryjoin="TransactionORM.wallet_to_id==WalletORM.wallet_id", back_populates="transactions_to"
    )


setup_relationships()
