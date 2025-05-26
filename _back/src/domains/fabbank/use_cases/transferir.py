from loguru import logger

from domains.fabbank.services.transaction import TransactionService
from domains.user.repositories.user import UserRepository
from shared.dto.error_code import FabbankError
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class Transferir:
    def __init__(self, ucr: UseCaseRequest):
        self.user_id = ucr.payload.get("user_id", None)
        self.args = ucr.payload.get("args", None)
        self.code = ucr.code

    def __call__(self) -> UseCaseResponse:
        args = self._parse_args()
        if len(args) <= 0:
            return UseCaseResponse(
                success=False,
                code=self.code,
                error_code=FabbankError.TRANSFER_WRONG_PARAMS,
            )

        if self.user_id is None:
            logger.error("ID do usuário não fornecido na requisição.")
            return UseCaseResponse(success=False, code=self.code, error_code=FabbankError.GENERIC_ERROR)

        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.user_id)
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
                code=self.code,
                data={"apelido": user.apelido},
                error_code=validate_response.error,
            )

        # Executar a transferência
        response = transaction_service.transfer_coins(user.id, user_to.id, args["value"], args["description"])

        if response.success:
            logger.info(
                f"Transferência realizada de {self.user_id} para {args['to_slack_id']}: {args['value']} F₵ - {args['description']}"
            )
            return UseCaseResponse(success=True, data=response.data, code=self.code)

        logger.error(f"Erro ao realizar a transferência: {response.error}")
        return UseCaseResponse(
            success=False,
            code=self.code,
            data={},
            error_code=response.error,
        )

    def _parse_args(self) -> dict | bool:
        # Verificar se os argumentos estão corretos
        if len(self.args) < 4:
            logger.error(f"Argumentos insuficientes para o comando: {self.args}")
            return {}

        # Extrair o usuário de destino
        to_user = self.args[1]
        if not to_user.startswith("<@") or not to_user.endswith(">"):
            logger.error(f"Formato inválido para o usuário de destino: {to_user}")
            return {}

        # Extrair o valor
        try:
            int(self.args[2])
        except ValueError:
            logger.error(f"Valor inválido para transferência: {self.args[2]}")
            return {}

        # Extrair a descrição
        description = self.args[3]
        if len(description) <= 0:
            logger.error(f"Formato inválido para a descrição: {description} ")
            return {}

        return {
            "to_slack_id": to_user[2:-1],
            "value": int(self.args[2]),
            "description": description,
        }
