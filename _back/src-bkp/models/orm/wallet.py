from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Wallet(Base):
    __tablename__ = "wallet"
    __table_args__ = {"schema": "fabbank"}

    wallet_id = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("public.users.id"), nullable=False)

    user = relationship("User", back_populates="wallet")

    transactions_from = relationship(
        "Transaction",
        foreign_keys="Transaction.wallet_from",
        back_populates="wallet_from_rel",
    )

    transactions_to = relationship(
        "Transaction",
        foreign_keys="Transaction.wallet_to",
        back_populates="wallet_to_rel",
    )

    def __str__(self) -> str:
        return f"Wallet({self.wallet_id}) - {self.balance} - Owner {self.user}"

    def __repr__(self) -> str:
        return f"Wallet({self.wallet_id}) - {self.balance} - Owner {self.user}"
