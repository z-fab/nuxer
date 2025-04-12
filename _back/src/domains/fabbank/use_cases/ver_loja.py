from loguru import logger

from domains.fabbank.services.store import StoreService
from domains.fabbank.services.wallet import WalletService
from domains.user.repositories.user import UserRepository
from interfaces.presenters.hints import FabbankHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class VerLoja:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        store_service = StoreService(db)
        list_items = store_service.get_all_enable_items()
        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.input.user_id)
        wallet_service = WalletService(db)
        response_balance = wallet_service.get_balance_info(user.id)

        if not response_balance.success:
            logger.error(f"Erro ao consultar o saldo: {response_balance.error}")
            return UseCaseResponse(
                success=False,
                data={},
                notification=[
                    {"presenter_hint": FabbankHints.LOJA_WALLET_NOT_FOUND},
                ],
            )

        logger.info(f"Loja consultada: {user.nome} - {response_balance.data['user_wallet'].balance} F₵")
        return UseCaseResponse(
            success=True,
            data={"all_items": list_items, "balance": response_balance.data["user_wallet"].balance},
            notification=[
                {"presenter_hint": FabbankHints.LOJA_OVERVIEW},
            ],
        )
