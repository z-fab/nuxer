from loguru import logger

from interfaces.presenters.slack.message.fabbank import FabbankSlackPresenter
from interfaces.presenters.slack.message.fabzenda import FabzendaSlackPresenter
from shared.dto.use_case_response import UseCaseResponse


class MessagePresenter:
    def __init__(self):
        self.fabbank = FabbankSlackPresenter()
        self.fabzenda = FabzendaSlackPresenter()
        self._registry = {
            ## Fabbank
            "fabbank.error": self.fabbank.generic_error,
            "fabbank.balance": self.fabbank.balance,
            "fabbank.balance_admin": self.fabbank.balance_admin,
            "fabbank.transfer_success": self.fabbank.transfer_success,
            "fabbank.transfer_notification": self.fabbank.transfer_notification,
            "fabbank.insufficient_balance": self.fabbank.insufficient_balance,
            "fabbank.wallet_not_found": self.fabbank.wallet_not_found,
            "fabbank.wrong_params": self.fabbank.wrong_params,
            "fabbank.transfer_error": self.fabbank.transfer_error,
            "fabbank.transfer_permission": self.fabbank.transfer_permission,
            ## Fabzenda
            "fabzenda.options": self.fabzenda.fabzenda_option,
        }

    def render(self, response: UseCaseResponse, presenter_hint: str) -> str:
        if presenter_hint in self._registry:
            return self._registry[presenter_hint](**response.data)

        logger.warning(f"Presenter hint '{presenter_hint}' não encontrado no registro.")
        return response.message or "Não consegui entender o que você quis dizer."
