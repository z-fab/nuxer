from loguru import logger

from interfaces.presenters.hints import FabbankHints
from interfaces.presenters.slack.message.fabbank import FabbankSlackPresenter
from shared.dto.use_case_response import UseCaseResponse


class MessagePresenter:
    def __init__(self):
        self.fabbank = FabbankSlackPresenter()
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
            # ## Fabbank
            # "fabbank.error": self.fabbank.generic_error,
            # "fabbank.balance": self.fabbank.balance,
            # "fabbank.balance_admin": self.fabbank.balance_admin,
            # "fabbank.transfer_success": self.fabbank.transfer_success,
            # "fabbank.transfer_notification": self.fabbank.transfer_notification,
            # "fabbank.insufficient_balance": self.fabbank.insufficient_balance,
            # "fabbank.wallet_not_found": self.fabbank.wallet_not_found,
            # "fabbank.wrong_params": self.fabbank.wrong_params,
            # "fabbank.transfer_error": self.fabbank.transfer_error,
            # "fabbank.transfer_permission": self.fabbank.transfer_permission,
            # ## Fabzenda
            # "fabzenda.options": self.fabzenda.fabzenda_option,
        }

    def render(self, response: UseCaseResponse, presenter_hint: str) -> str:
        if presenter_hint in self._registry:
            return self._registry[presenter_hint](**response.data)

        logger.warning(f"Presenter hint '{presenter_hint}' não encontrado no registro.")
        return response.message or "Não consegui entender o que você quis dizer."
