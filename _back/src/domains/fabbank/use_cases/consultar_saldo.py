from loguru import logger

from domains.fabbank.repositories.wallet import WalletRepository
from domains.fabbank.services.wallet import WalletService
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class ConsultarSaldo:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        try:
            wallet_service = WalletService(WalletRepository(db))
            response = wallet_service.get_balance_info(self.input.user_id)

            if response.success:
                if "total_balance" not in response.data:
                    logger.info(
                        f"Saldo consultado: {response.data['wallet'].user.nome} - {response.data['wallet'].balance} F₵"
                    )
                    return UseCaseResponse(
                        success=True, data=response.data, notification=[{"presenter_hint": "fabbank.balance"}]
                    )

                # Se o usuário for admin, retorna o saldo total
                logger.info(f"Saldo consultado para {self.input.user_id}: {response.data}")
                return UseCaseResponse(
                    success=True, data=response.data, notification=[{"presenter_hint": "fabbank.balance_admin"}]
                )

            return UseCaseResponse(success=False, notification=[{"presenter_hint": response.error}])

        except Exception as e:
            logger.error(f"Erro ao consultar o saldo para {self.input.user_id}: {e}")
            return UseCaseResponse(success=False, notification=[{"presenter_hint": "fabbank.error"}])
