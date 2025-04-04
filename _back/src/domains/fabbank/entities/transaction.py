from datetime import datetime

from pydantic import BaseModel

from domains.fabbank.entities.wallet import WalletEntity


class TransactionEntity(BaseModel):
    model_config = {"from_attributes": True}

    transaction_id: str
    wallet_from_id: str
    wallet_to_id: int
    amount: int
    description: str
    timestamp: datetime | None = None

    wallet_from: WalletEntity | None = None
    wallet_to: WalletEntity | None = None
