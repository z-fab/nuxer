from loguru import logger

from domains.fabbank import messages as MSG
from domains.fabbank.services.transaction import TransactionService
from domains.user.repositories.user import UserRepository
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class AlterarSaldo:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        try:
            parsed_args, args = self._parse_args()
            if not parsed_args:
                return UseCaseResponse(success=False, notification=[{"presenter_hint": "fabbank.wrong_params"}])

            user_respository = UserRepository(db)
            user = user_respository.get_user_by_slack_id(self.input.user_id)
            user_to = user_respository.get_user_by_slack_id(args["to_slack_id"])

            transaction_service = TransactionService(db)
            response = transaction_service.change_coins(user.id, user_to.id, args["value"], args["description"])

            if response.success:
                logger.info(
                    f"Transferência realizada de {self.input.user_id} para {args['to_slack_id']}: {args['value']} F₵ - {args['description']}"
                )
                return UseCaseResponse(
                    success=True,
                    data=response.data,
                    notification=[
                        {"presenter_hint": "fabbank.transfer_success"},
                        {"presenter_hint": "fabbank.transfer_notification", "user": response.data["wallet_to"].user},
                    ],
                )

            return UseCaseResponse(
                success=False,
                data={},
                notification=[{"presenter_hint": f"fabbank.{response.error}"}],
            )

        except Exception as e:
            logger.error(f"Erro ao realizar a transferência: {e}")
            return UseCaseResponse(
                success=False,
                data=response.data,
                notification=[{"presenter_hint": "fabbank.transfer_error"}],
            )

    def _parse_args(self) -> dict | bool:
        # Verificar se os argumentos estão corretos
        if len(self.input.args) < 3:
            logger.debug(f"Argumentos insuficientes para o comando: {self.input.args}")
            return False, MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS

        # Extrair o usuário de destino
        to_user = self.input.args[1]
        if not to_user.startswith("<@") or not to_user.endswith(">"):
            logger.debug(f"Formato inválido para o usuário de destino: {to_user}")
            return False, MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS

        # Extrair o valor
        try:
            int(self.input.args[2])
        except ValueError:
            logger.debug(f"Valor inválido para transferência: {self.input.args[2]}")
            return False, MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS

        # Extrair a descrição
        description = self.input.args[3]
        if len(description) <= 0:
            logger.debug(f"Formato inválido para a descrição: {description} ")
            return False, MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS

        return True, {
            "to_slack_id": to_user[2:-1],
            "value": int(self.input.args[2]),
            "description": description,
        }
