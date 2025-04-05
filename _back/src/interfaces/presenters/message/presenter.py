from interfaces.presenters.message.fabbank import FabbankSlackPresenter
from shared.dto.use_case_response import UseCaseResponse


class SlackPresenter:
    def __init__(self):
        self.fabbank = FabbankSlackPresenter()
        self._registry = {
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
        }

    def render(self, response: UseCaseResponse, presenter_hint: str) -> str:
        if presenter_hint in self._registry:
            return self._registry[presenter_hint](**response.data)

        return response.message or "Mensagem não especificada"
