from loguru import logger

from domains.fabbank.services.wallet import WalletService
from domains.user.repositories.user import UserRepository
from shared.dto.error_code import FabbankError
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class ConsultarSaldo:
    def __init__(self, ucr: UseCaseRequest):
        self.user_id = ucr.payload.get("user_id", None)
        self.code = ucr.code

    def __call__(self) -> UseCaseResponse:
        if self.user_id is None:
            logger.error("ID do usuário não fornecido na requisição.")
            return UseCaseResponse(success=False, code=self.code, error_code=FabbankError.GENERIC_ERROR)

        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.user_id)
        wallet_service = WalletService(db)
        response = wallet_service.get_balance_info(user.id)

        if not response.success:
            return UseCaseResponse(
                code=self.code,
                success=False,
                data={"apelido": user.apelido},
                error_code=response.error,
            )

        # Se o usuário for admin, retorna o saldo total
        logger.info(f"Saldo consultado para o usuário {user.nome} (ID {user.id}): {response.data['total_balance']}")
        return UseCaseResponse(code=self.code, success=True, data=response.data)
