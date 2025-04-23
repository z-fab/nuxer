from enum import Enum

from loguru import logger

from interfaces.presenters.hints import FabbankHints, FabzendaHints
from interfaces.presenters.slack.message.fabbank import FabbankSlackPresenter
from interfaces.presenters.slack.message.fabzenda import FabzendaSlackPresenter


class MessagePresenter:
    def __init__(self):
        self.fabbank = FabbankSlackPresenter()
        self.fabzenda = FabzendaSlackPresenter()
        self._registry = {
            FabbankHints.BALANCE: self.fabbank.balance,
            FabbankHints.BALANCE_ADMIN: self.fabbank.balance_admin,
            FabbankHints.BALANCE_WALLET_NOT_FOUND: self.fabbank.balance_wallet_not_found,
            ##
            FabbankHints.TRANSFER_SUCCESS: self.fabbank.transfer_success,
            FabbankHints.TRANSFER_SUCCESS_NOTIFICATION: self.fabbank.transfer_success_notification,
            FabbankHints.TRANSFER_WRONG_PARAMS: self.fabbank.transfer_wrong_params,
            FabbankHints.TRANSFER_WALLET_NOT_FOUND: self.fabbank.transfer_wrong_params,
            FabbankHints.TRANSFER_INSUFFICIENT_BALANCE: self.fabbank.transfer_insufficient_balance,
            FabbankHints.TRANSFER_ERROR: self.fabbank.transfer_error,
            FabbankHints.TRANSFER_PERMISSION_DENIED: self.fabbank.transfer_permission,
            ##
            FabbankHints.LOJA_OPTIONS: self.fabbank.loja_options,
            FabbankHints.LOJA_OVERVIEW: self.fabbank.loja_overview,
            ##
            FabzendaHints.FAZENDA_OPTIONS: self.fabzenda.fabzenda_option,
            ##
            FabzendaHints.NOTIFICATE_ANIMAL_DEAD: self.fabzenda.notificate_animal_dead,
            FabzendaHints.NOTIFICATE_CHANNEL_ANIMAL_DEAD: self.fabzenda.notificate_channel_animal_dead,
            FabzendaHints.NOTIFICATE_ANIMAL_SICK: self.fabzenda.notificate_animal_sick,
            FabzendaHints.NOTIFICATE_CHANNEL_LOTTERY: self.fabzenda.notificate_channel_lottery,
            FabzendaHints.NOTIFICATE_LOTTERY: self.fabzenda.notificate_lottery,
        }

    def render(self, data: dict, presenter_hint: Enum) -> str:
        if presenter_hint in self._registry:
            return self._registry[presenter_hint](**data)

        logger.warning(f"Presenter hint '{presenter_hint}' não encontrado no registro.")
        return "Não consegui entender o que você quis dizer."
