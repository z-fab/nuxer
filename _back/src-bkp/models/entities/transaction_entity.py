from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.entities.wallet_entity import WalletEntity
from models.entities.user_entity import UserEntity


@dataclass
class TransactionEntity:
    transaction_id: str
    wallet_from: WalletEntity
    wallet_to: WalletEntity
    amount: int
    description: str
    timestamp: datetime

