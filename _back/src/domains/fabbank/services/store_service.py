from config.const import CONST_ERROR
from repositories import fabbank_repository as fbr
from repositories.configs_repository import get_config_by_name, save_config_value

from models.entities.item_loja_entity import ItemLojaEntity
from models.entities.user_entity import UserEntity

from .price_calculation_service import PriceCalculationService


class StoreService:
    def __init__(self, user: UserEntity):
        self.user = user
        self.price_service = PriceCalculationService(self._get_total_coins())

    def purchase_item(self, item: ItemLojaEntity) -> bool:
        self._validate_item(item)

        wallet = fbr.get_wallet_by_user_id(self.user.id)
        value = self.price_service.calculate_price(item)

        self._validate_purchase(wallet, item, value)

        result = self._execute_purchase(wallet, item, value)
        if not result:
            raise RuntimeError(CONST_ERROR.FABBANK_LOJA_FAILED)

        return True

    def _validate_item(self, item: ItemLojaEntity):
        if item is None:
            raise ValueError(CONST_ERROR.FABBANK_LOJA_ITEM_NOT_FOUND)
        if item.amount == 0 or not item.enable:
            raise ValueError(CONST_ERROR.FABBANK_LOJA_ITEM_UNAVAILABLE)

    def _validate_purchase(self, wallet, item: ItemLojaEntity, value: int):
        if int(wallet.balance) < item.valor:
            raise ValueError(CONST_ERROR.FABBANK_LOJA_INSUFFICIENT_BALANCE)

    def _execute_purchase(self, wallet, item: ItemLojaEntity, value: int) -> bool:
        result = fbr.remove_coins(wallet, value)

        if result and item.valor_real:
            self._update_real_reserve(item.valor)

        if result:
            fbr.create_transaction(
                fbr.get_wallet_by_user_id(0),
                wallet,
                value * (-1),
                f"Compra de item na Lojinha do Nuxer: {item.nome}",
            )

        return result

    def _update_real_reserve(self, valor: int):
        reserva_real_orm = get_config_by_name("RESERVA_REAL")
        save_config_value(
            reserva_real_orm,
            str(int(reserva_real_orm.value) - valor),
        )

    def _get_total_coins(self) -> int:
        all_wallets = fbr.get_all_wallets()
        return sum(wallet.balance for wallet in all_wallets)
