from enum import Enum

from loguru import logger

from interfaces.presenters.hints import FabbankHints, FabzendaHints
from interfaces.presenters.slack.view.fabbank import FabbankSlackPresenter
from interfaces.presenters.slack.view.fabzenda import FabzendaSlackPresenter


class ViewPresenter:
    def __init__(self):
        self.fabzenda = FabzendaSlackPresenter()
        self.fabbank = FabbankSlackPresenter()
        self._registry = {
            FabbankHints.LOJA_OVERVIEW: self.fabbank.loja_overview,
            FabbankHints.LOJA_BUY_SUCCESS: self.fabbank.loja_buy_success,
            FabbankHints.LOJA_BUY_ADMIN: self.fabbank.loja_buy_admin,
            FabbankHints.LOJA_BUY_ERROR: self.fabbank.loja_buy_error,
            FabbankHints.LOJA_INSUFFICIENT_BALANCE: self.fabbank.loja_insufficient_balance,
            FabbankHints.LOJA_ITEM_PRICE_CHANGED: self.fabbank.loja_item_price_changed,
            FabbankHints.LOJA_ITEM_UNAVAILABLE: self.fabbank.loja_item_unavailable,
            FabbankHints.LOJA_WALLET_NOT_FOUND: self.fabbank.loja_wallet_not_found,
            ##
            FabzendaHints.FAZENDA_OVERVIEW: self.fabzenda.fazenda_overview,
            FabzendaHints.FAZENDA_OVERVIEW_VAZIA: self.fabzenda.fazenda_overview_vazia,
            FabzendaHints.FAZENDA_OVERVIEW_DETALHE_ANIMAL: self.fabzenda.fazenda_overview_detalhe_animal,
            ##
            FabzendaHints.STORE_OVERVIEW: self.fabzenda.store_overview,
            FabzendaHints.STORE_WALLET_NOT_FOUND: self.fabzenda.store_wallet_not_found,
            FabzendaHints.STORE_DETALHE_ITEM: self.fabzenda.store_detalhe_item,
            FabzendaHints.STORE_BUY_SUCCESS: self.fabzenda.store_buy_success,
            FabzendaHints.STORE_TRANSACTION_ERROR: self.fabzenda.store_transaction_error,
            FabzendaHints.STORE_ITEM_UNAVAILABLE: self.fabzenda.store_item_not_available,
            FabzendaHints.STORE_INSUFFICIENT_BALANCE: self.fabzenda.store_insufficient_balance,
            FabzendaHints.STORE_BUY_ERROR: self.fabzenda.store_buy_error,
            ##
            FabzendaHints.CELEIRO_OVERVIEW: self.fabzenda.celeiro_overview,
            FabzendaHints.CELEIRO_DETALHE_ANIMAL: self.fabzenda.celeiro_detalhe_animal,
            FabzendaHints.CELEIRO_MAX_ANIMALS_REACHED: self.fabzenda.celeiro_max_animals_reached,
            FabzendaHints.CELEIRO_INSUFFICIENT_BALANCE: self.fabzenda.celeiro_insufficient_balance,
            FabzendaHints.CELEIRO_ANIMAL_TYPE_NOT_AVAILABLE: self.fabzenda.celeiro_animal_type_not_available,
            FabzendaHints.CELEIRO_TRANSACTION_ERROR: self.fabzenda.celeiro_transaction_error,
            FabzendaHints.CELEIRO_CREATED_ERROR: self.fabzenda.celeiro_created_error,
            FabzendaHints.CELEIRO_WALLET_NOT_FOUND: self.fabzenda.celeiro_wallet_not_found,
            FabzendaHints.CELEIRO_ANIMAL_BUY_SUCCESS: self.fabzenda.celeiro_compra_animal,
            ##
            FabzendaHints.FEED_INSUFFICIENT_BALANCE: self.fabzenda.alimentar_insufficient_balance,
            FabzendaHints.FEED_ANIMAL_DEAD: self.fabzenda.alimentar_animal_dead,
            FabzendaHints.FEED_TRANSACTION_ERROR: self.fabzenda.alimentar_transaction_error,
            FabzendaHints.FEED_ERROR: self.fabzenda.alimentar_error,
            FabzendaHints.FEED_SUCCESS: self.fabzenda.alimentar_animal,
            ##
            FabzendaHints.BURIAL_INSUFFICIENT_BALANCE: self.fabzenda.enterrar_insufficient_balance,
            FabzendaHints.BURIAL_ANIMAL_LIVES: self.fabzenda.enterrar_animal_lives,
            FabzendaHints.BURIAL_TRANSACTION_ERROR: self.fabzenda.enterrar_transaction_error,
            FabzendaHints.BURIAL_ERROR: self.fabzenda.enterrar_error,
            FabzendaHints.BURIAL_SUCCESS: self.fabzenda.enterrar_animal,
            ##
            FabzendaHints.ABDUCTION_ANIMAL_LIVES: self.fabzenda.abduzir_animal_lives,
            FabzendaHints.ABDUCTION_TRANSACTION_ERROR: self.fabzenda.abduzir_transaction_error,
            FabzendaHints.ABDUCTION_ERROR: self.fabzenda.abduzir_error,
            FabzendaHints.ABDUCTION_SUCCESS: self.fabzenda.abduzir_animal,
        }

    def render(self, data: dict, presenter_hint: Enum) -> str:
        if presenter_hint in self._registry:
            return self._registry[presenter_hint](**data)

        logger.warning(f"Presenter hint '{presenter_hint}' não encontrado no registro.")
        return "Nuxer", "Não consegui entender o que você quis dizer."
