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
            FabbankHints.TRANSFER_PERMISSION_DENIED: self.fabbank.transfer_permission,
            ##
            FabbankHints.LOJA_OPTIONS: self.fabbank.loja_options,
            FabbankHints.LOJA_OVERVIEW: self.fabbank.loja_overview,
        }

    def render(self, response: UseCaseResponse, presenter_hint: str) -> str:
        if presenter_hint in self._registry:
            return self._registry[presenter_hint](**response.data)

        logger.warning(f"Presenter hint '{presenter_hint}' não encontrado no registro.")
        return response.message or "Não consegui entender o que você quis dizer."
