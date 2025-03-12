from models.orm.transaction import Transaction
from models.entities.transaction_entity import TransactionEntity


class TransactionMapper:
    @staticmethod
    def orm_to_entity(orm_transaction: Transaction) -> TransactionEntity:
        return TransactionEntity(
            transaction_id=orm_transaction.transaction_id,
            wallet_from=orm_transaction.wallet_from,
            wallet_to=orm_transaction.wallet_to,
            amount=orm_transaction.amount,
            description=orm_transaction.description,
            timestamp=orm_transaction.timestamp,
        )