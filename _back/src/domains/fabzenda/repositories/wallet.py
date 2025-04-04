from domains.fabbank.entities.wallet import WalletEntity
from domains.fabbank.orm.wallet import WalletORM
from domains.user.orm.user import UserORM
from shared.infrastructure.db_context import DatabaseExternal


class WalletRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def get_all_wallets(self) -> list[WalletEntity] | list[None]:
        with self._db_session() as session:
            orm = session.query(WalletORM).all()
            return [WalletEntity.model_validate(w) for w in orm]

    def get_wallet_by_user_id(self, user_id: str) -> WalletEntity | None:
        with self._db_session() as session:
            orm = session.query(WalletORM).filter(WalletORM.user_id == user_id).first()
            return WalletEntity.model_validate(orm)

    def get_wallet_by_slack_id(self, slack_id: str) -> WalletEntity | None:
        with self._db_session() as session:
            orm = (
                session.query(WalletORM)
                .join(WalletORM.user)
                .filter(UserORM.slack_id == slack_id)
                .order_by(UserORM.id.desc())
                .first()
            )

            if not orm:
                return None

            return WalletEntity.model_validate(orm)

    def add_coins(self, wallet: WalletEntity, value: int) -> bool:
        with self._db_session() as session:
            orm = session.query(WalletORM).filter(WalletORM.wallet_id == wallet.wallet_id).first()
            if not orm:
                return False

            orm.balance += value
            session.commit()
            return True

    def remove_coins(self, wallet: WalletEntity, value: int) -> bool:
        with self._db_session() as session:
            orm = session.query(WalletORM).filter(WalletORM.wallet_id == wallet.wallet_id).first()
            if not orm:
                return False

            if orm.balance < value:
                return False

            orm.balance -= value
            session.commit()
            return True
