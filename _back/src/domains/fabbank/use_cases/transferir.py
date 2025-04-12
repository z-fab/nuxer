from loguru import logger

from domains.fabbank import messages as MSG
from domains.fabbank.services.transaction import TransactionService
from domains.user.repositories.user import UserRepository
from interfaces.presenters.hints import FabbankHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class Transferir:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        parsed_args, args = self._parse_args()
        if not parsed_args:
            return UseCaseResponse(success=False, notification=[{"presenter_hint": FabbankHints.TRANSFER_WRONG_PARAMS}])

        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.input.user_id)
        user_to = user_repository.get_user_by_slack_id(args["to_slack_id"])

        transaction_service = TransactionService(db)

        # Verificar se a transação pode ser feita
        validate_response = transaction_service.validate_transfer_coins(
            from_id=user.id, to_id=user_to.id, value=args["value"], description=args["description"]
        )

        if not validate_response.success:
            logger.error(f"Erro ao validar a transferência: {validate_response.error}")
            return UseCaseResponse(
                success=False,
                data={"apelido": user.apelido},
                notification=[
                    {"presenter_hint": validate_response.error},
                ],
            )

        # Executar a transferência
        response = transaction_service.transfer_coins(user.id, user_to.id, args["value"], args["description"])

        if response.success:
            logger.info(
                f"Transferência realizada de {self.input.user_id} para {args['to_slack_id']}: {args['value']} F₵ - {args['description']}"
            )
            return UseCaseResponse(
                success=True,
                data=response.data,
                notification=[
                    {"presenter_hint": FabbankHints.TRANSFER_SUCCESS},
                    {
                        "presenter_hint": FabbankHints.TRANSFER_SUCCESS_NOTIFICATION,
                        "user": response.data["wallet_to"].user,
                    },
                ],
            )

        logger.error(f"Erro ao realizar a transferência: {response.error}")
        return UseCaseResponse(
            success=False,
            data={},
            notification=[{"presenter_hint": response.error}],
        )

    def _parse_args(self) -> dict | bool:
        # Verificar se os argumentos estão corretos
        if len(self.input.args) < 3:
            logger.error(f"Argumentos insuficientes para o comando: {self.input.args}")
            return False, MSG.TRANSFER_WRONG_PARAMS

        # Extrair o usuário de destino
        to_user = self.input.args[1]
        if not to_user.startswith("<@") or not to_user.endswith(">"):
            logger.error(f"Formato inválido para o usuário de destino: {to_user}")
            return False, MSG.TRANSFER_WRONG_PARAMS

        # Extrair o valor
        try:
            int(self.input.args[2])
        except ValueError:
            logger.error(f"Valor inválido para transferência: {self.input.args[2]}")
            return False, MSG.TRANSFER_WRONG_PARAMS

        # Extrair a descrição
        description = self.input.args[3]
        if len(description) <= 0:
            logger.error(f"Formato inválido para a descrição: {description} ")
            return False, MSG.TRANSFER_WRONG_PARAMS

        return True, {
            "to_slack_id": to_user[2:-1],
            "value": int(self.input.args[2]),
            "description": description,
        }
