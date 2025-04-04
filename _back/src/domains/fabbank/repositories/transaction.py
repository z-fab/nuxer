import uuid
from datetime import datetime

from loguru import logger

from domains.fabbank.entities.wallet import WalletEntity
from domains.fabbank.orm.transaction import TransactionORM
from shared.infrastructure.db_context import DatabaseExternal


class TransactionRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def create_transaction(
        self, wallet_from: WalletEntity, wallet_to: WalletEntity, value: int, description: str
    ) -> bool:
        transaction = TransactionORM(
            transaction_id=str(uuid.uuid4()),
            wallet_from_id=wallet_from.wallet_id,
            wallet_to_id=wallet_to.wallet_id,
            amount=value,
            description=description,
            timestamp=datetime.now(),
        )

        try:
            with self._db_session() as session:
                session.add(transaction)
                session.commit()
            return True
        except Exception as e:
            logger.warning(f"Erro ao criar a transação: {e}")
            return False
