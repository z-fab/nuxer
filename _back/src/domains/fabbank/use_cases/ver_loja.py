from loguru import logger

from domains.fabbank.services.store import StoreService
from domains.fabbank.services.wallet import WalletService
from domains.user.repositories.user import UserRepository
from shared.dto.error_code import FabbankError
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class VerLoja:
    def __init__(self, ucr: UseCaseRequest):
        self.user_id = ucr.payload.get("user_id", None)
        self.args = ucr.payload.get("args", None)
        self.code = ucr.code

    def __call__(self) -> UseCaseResponse:
        if self.user_id is None:
            logger.error("ID do usuário não fornecido na requisição.")
            return UseCaseResponse(success=False, code=self.code, error_code=FabbankError.GENERIC_ERROR)

        store_service = StoreService(db)
        list_items = store_service.get_all_enable_items()
        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.user_id)
        wallet_service = WalletService(db)
        response_balance = wallet_service.get_balance_info(user.id)

        if not response_balance.success:
            logger.error(f"Erro ao consultar o saldo: {response_balance.error}")
            return UseCaseResponse(
                success=False,
                code=self.code,
                error_code=response_balance.error,
            )

        logger.info(f"Loja consultada: {user.nome} - {response_balance.data['user_wallet'].balance} F₵")
        return UseCaseResponse(
            success=True,
            code=self.code,
            data={"all_items": list_items, "balance": response_balance.data["user_wallet"].balance},
        )
