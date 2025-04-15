from datetime import datetime

from domains.config.repositories.config import ConfigRepository
from domains.fabbank.entities.item_loja import ItemLojaEntity
from domains.fabbank.repositories.store import StoreRepository
from domains.fabbank.repositories.transaction import TransactionRepository
from domains.fabbank.repositories.wallet import WalletRepository
from interfaces.presenters.hints import FabbankHints
from shared.dto.service_response import ServiceResponse
from shared.infrastructure.db_context import DatabaseExternal


class StoreService:
    def __init__(self, db_context: DatabaseExternal):
        self.transaction_repository = TransactionRepository(db_context)
        self.wallet_repository = WalletRepository(db_context)
        self.item_repository = StoreRepository(db_context)
        self.config_repository = ConfigRepository(db_context)

    def get_all_enable_items(self) -> list[ItemLojaEntity]:
        item_list = self.item_repository.get_all_enabled_items()

        if not item_list:
            return ServiceResponse(
                success=False,
                error=FabbankHints.LOJA_NO_ITEMS,
            )

        for item in item_list:
            item = self._calculate_price(item)

        return item_list

    def _calculate_price(self, item: ItemLojaEntity) -> ItemLojaEntity:
        if not item.valor_real:
            return item.valor

        reserva_real = int(self.config_repository.get_config_by_name("RESERVA_REAL").value)
        reserva_segura = reserva_real * 0.9
        total_coins = self.wallet_repository.get_total_coins()

        # Calcula a taxa de câmbio base com base na quantidade total de moedas disponíveis e a reserva real
        taxa_cambio_base = total_coins / reserva_real

        # Determina a proporção da reserva que já foi usada, limitada entre 0 e 1
        proporcao_reserva_usada = max(0, min(1, (reserva_real - reserva_segura) / reserva_real))

        # Define um fator de escassez que aumenta exponencialmente à medida que a reserva se aproxima do limite seguro
        fator_escassez = 1 + (1 - proporcao_reserva_usada) ** 2

        # Aplica um fator semanal com leve variação entre segunda (0.95) e domingo (~1.06)
        fator_semanal = 0.95 + (datetime.now().weekday() / 60)

        # Aplica um fator baseado no horário atual, favorecendo compras próximas às 14h
        hora = datetime.now().hour
        fator_horario = (
            1.0 + (min(abs(14 - hora), 5) * 0.02) if 11 <= hora < 17 else 0.9 + (min(hora, 24 - hora) * 0.01)
        )

        # Cálculo final do valor do item com todos os fatores aplicados
        valor = round(item.valor * taxa_cambio_base * fator_escassez * fator_semanal * fator_horario)
        item.valor = valor

        return item

    def purchase_item(self, user_id: int, cod: str) -> ServiceResponse:
        wallet = self.wallet_repository.get_wallet_by_user_id(user_id)
        item = self.get_item_by_cod(cod)

        if not self.wallet_repository.remove_coins(wallet, item.valor):
            return ServiceResponse(
                success=False,
                error=FabbankHints.LOJA_BUY_ERROR,
            )

        reserva_real = self.config_repository.get_config_by_name("RESERVA_REAL")
        reserva_real.value = str(int(reserva_real.value) - item.valor)
        self.config_repository.save_config(reserva_real)

        # Update item amount
        if item.amount > 0:
            item.amount -= 1
            self.item_repository.save_item(item)

        return ServiceResponse(
            success=True,
            data={"item": item},
        )

    def can_purchase_item(self, user_id: int, item_id: int, price: int) -> ServiceResponse:
        wallet = self.wallet_repository.get_wallet_by_user_id(user_id)
        item = self.get_item_by_cod(item_id)

        # Validate if the wallet exists
        if not wallet:
            return ServiceResponse(success=False, error=FabbankHints.LOJA_WALLET_NOT_FOUND)

        # Validate if the item is available
        if not item or item.amount == 0 or not item.enable:
            return ServiceResponse(success=False, error=FabbankHints.LOJA_ITEM_UNAVAILABLE)

        # Validate if the user has enough balance
        if wallet.balance < item.valor:
            return ServiceResponse(success=False, error=FabbankHints.LOJA_INSUFFICIENT_BALANCE)

        if item.valor != price:
            return ServiceResponse(success=False, error=FabbankHints.LOJA_ITEM_PRICE_CHANGED)

        return ServiceResponse(success=True)

    def get_item_by_cod(self, cod: str) -> ItemLojaEntity | None:
        item = self.item_repository.get_item_by_cod(cod)
        item = self._calculate_price(item)

        if not item:
            return None

        return item
