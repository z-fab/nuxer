import uuid
from datetime import datetime

from loguru import logger

from externals.context import Context
from models.entities.item_loja_entity import ItemLojaEntity
from models.entities.wallet_entity import WalletEntity
from models.mappers.item_loja_mapper import ItemLojaMapper
from models.mappers.wallet_mapper import WalletMapper
from models.orm.item_loja import ItemLoja
from models.orm.transaction import Transaction
from models.orm.wallet import Wallet

context = Context()


## GETTERS
def get_all_wallets() -> list[WalletEntity]:
    with context.db.session() as session:
        wallets = session.query(Wallet).all()
        session.expunge_all()
        return [WalletMapper.orm_to_entity(wallet) for wallet in wallets]


def get_wallet_by_id(wallet_id: str) -> WalletEntity:
    with context.db.session() as session:
        wallet = session.query(Wallet).filter(Wallet.wallet_id == wallet_id).first()
        session.expunge(wallet)
        return WalletMapper.orm_to_entity(wallet)


def get_wallet_by_user_id(
    user_id: str | list[str],
) -> WalletEntity | list[WalletEntity]:
    list_user_id = user_id
    if isinstance(user_id, int) or isinstance(user_id, str):
        list_user_id = [user_id]

    with context.db.session() as session:
        wallet = session.query(Wallet).filter(Wallet.user_id.in_(list_user_id)).all()
        session.expunge_all()

        if not wallet:
            return None

        wallet_entity = [WalletMapper.orm_to_entity(wallet) for wallet in wallet]

    return wallet_entity if len(wallet_entity) > 1 else wallet_entity[0]


def get_item_by_cod(cod: str) -> ItemLojaEntity:
    with context.db.session() as session:
        item = session.query(ItemLoja).filter(ItemLoja.cod == cod).first()
        session.expunge(item)
        if not item:
            return None

        return ItemLojaMapper.orm_to_entity(item)


def get_all_enabled_items() -> ItemLojaEntity:
    with context.db.session() as session:
        item_list = session.query(ItemLoja).filter(ItemLoja.enable).all()
        session.expunge_all()
        if not item_list:
            return None

        return [ItemLojaMapper.orm_to_entity(item) for item in item_list]


## SETTERS
def remove_coins(wallet: WalletEntity, value: int):
    # Verifica se o saldo é suficiente
    if int(wallet.balance) < int(value):
        return False

    # Verificar se é FBA001
    if wallet.wallet_id == "FBA001":
        return True

    wallet.balance = int(wallet.balance) - int(value)

    try:
        with context.db.session() as session:
            session.merge(WalletMapper.entity_to_orm(wallet))
            session.commit()
        return True
    except Exception as e:
        logger.warning(f"Erro ao remover os fabcoins: {e}")
        return False


def add_coins(wallet: WalletEntity, value: int):
    # Verificar se é FBA001
    if wallet.wallet_id == "FBA001":
        return True

    wallet.balance = int(wallet.balance) + int(value)

    try:
        with context.db.session() as session:
            session.merge(WalletMapper.entity_to_orm(wallet))
            session.commit()
        return True
    except Exception as e:
        logger.warning(f"Erro ao adicionar os fabcoins: {e}")
        return False


def create_transaction(wallet_from: WalletEntity, wallet_to: WalletEntity, value: int, description: str):
    transaction = Transaction(
        transaction_id=str(uuid.uuid4()),
        wallet_from=wallet_from.wallet_id,
        wallet_to=wallet_to.wallet_id,
        amount=value,
        description=description,
        timestamp=datetime.now(),
    )

    try:
        with context.db.session() as session:
            session.add(transaction)
            session.commit()
        return True
    except Exception as e:
        logger.warning(f"Erro ao criar a transação: {e}")
        return False


# def get_transactions_by_wallet_to(wallet_id: str) -> list[TransactionEntity]:
#     with context.db.session() as session:
#         transactions = (
#             session.query(Transaction)
#             .filter(Transaction.wallet_to == wallet_id)
#             .order_by(Transaction.timestamp.desc())
#             .all()
#         )
#         session.expunge_all()
#         return [TransactionMapper.orm_to_entity(transaction) for transaction in transactions]
