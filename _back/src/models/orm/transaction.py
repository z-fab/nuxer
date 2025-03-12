from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Transaction(Base):
    __tablename__ = "transaction"
    __table_args__ = {"schema": "fabbank"}

    transaction_id = Column(String, primary_key=True)
    wallet_from = Column(String, ForeignKey("fabbank.wallet.wallet_id"), nullable=False)
    wallet_to = Column(String, ForeignKey("fabbank.wallet.wallet_id"), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    # Relationships
    wallet_from_rel = relationship(
        "Wallet",
        foreign_keys="Transaction.wallet_from",
        back_populates="transactions_from",
    )
    wallet_to_rel = relationship("Wallet", foreign_keys="Transaction.wallet_to", back_populates="transactions_to")

    def __str__(self) -> str:
        return f"Transaction({self.transaction_id}) - {self.amount} from {self.wallet_from} to {self.wallet_to}"

    def __repr__(self) -> str:
        return f"Tansaction({self.transaction_id}) - {self.amount} from {self.wallet_from} to {self.wallet_to}"
