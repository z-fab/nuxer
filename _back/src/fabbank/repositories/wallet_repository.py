from models.entities.wallet_entity import WalletEntity
from models.orm.wallet import WalletORM
from shared.infrastructure.db_context import DatabaseExternal


class WalletRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def get_wallet_by_user_id(self, user_id: str) -> WalletEntity:
        with self._db_session() as session:
            orm = session.query(WalletORM).filter(WalletORM.user_id == user_id).first()
            return WalletEntity.from_orm(orm)
