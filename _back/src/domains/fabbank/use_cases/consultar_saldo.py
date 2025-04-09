from loguru import logger

from domains.fabbank.services.wallet import WalletService
from domains.user.repositories.user import UserRepository
from interfaces.presenters.hints import FabbankHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class ConsultarSaldo:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.input.user_id)
        wallet_service = WalletService(db)
        response = wallet_service.get_balance_info(user.id)

        if not response.success:
            return UseCaseResponse(
                success=False,
                data={"apelido": user.apelido},
                notification=[
                    {"presenter_hint": response.error},
                ],
            )

        if "total_balance" not in response.data:
            logger.info(
                f"Saldo consultado: {response.data['user_wallet'].user.nome} - {response.data['user_wallet'].balance} F₵"
            )
            return UseCaseResponse(
                success=True, data=response.data, notification=[{"presenter_hint": FabbankHints.BALANCE}]
            )

        # Se o usuário for admin, retorna o saldo total
        logger.info(f"Saldo consultado para {self.input.user_id}: {response.data}")
        return UseCaseResponse(
            success=True, data=response.data, notification=[{"presenter_hint": FabbankHints.BALANCE_ADMIN}]
        )
