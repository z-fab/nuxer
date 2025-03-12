from models.entities.wallet_entity import WalletEntity
from models.orm.wallet import Wallet
from repositories.users_repository import get_users_by_id


class WalletMapper:
    @staticmethod
    def orm_to_entity(orm_wallet: Wallet) -> WalletEntity:
        return WalletEntity(
            wallet_id=orm_wallet.wallet_id,
            balance=orm_wallet.balance,
            user=get_users_by_id(orm_wallet.user_id),
        )

    @staticmethod
    def entity_to_orm(entity_wallet: WalletEntity) -> Wallet:
        return Wallet(
            wallet_id=entity_wallet.wallet_id,
            balance=entity_wallet.balance,
            user_id=entity_wallet.user.id,
        )
