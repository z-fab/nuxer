from loguru import logger

from domains.fabbank.services.store import StoreService
from domains.user.repositories.user import UserRepository
from shared.dto.error_code import FabbankError
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class ComprarItem:
    def __init__(self, ucr: UseCaseRequest):
        self.user_id = ucr.payload.get("user_id", None)
        self.args = ucr.payload.get("args", None)
        self.code = ucr.code

    def __call__(self) -> UseCaseResponse:
        if self.user_id is None:
            logger.error("ID do usuário não fornecido na requisição.")
            return UseCaseResponse(success=False, code=self.code, error_code=FabbankError.GENERIC_ERROR)

        if len(self.args) < 3:
            logger.error("Parâmetros insuficientes para a compra do item.")
            return UseCaseResponse(
                success=False,
                code=self.code,
                error_code=FabbankError.GENERIC_ERROR,
            )

        store_service = StoreService(db)
        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.user_id)

        cod_item = self.args[1]
        price = int(self.args[2])

        response_can_purchase = store_service.can_purchase_item(user.id, cod_item, price)
        if not response_can_purchase.success:
            logger.error(f"Erro ao validar a compra: {response_can_purchase.error}")
            return UseCaseResponse(success=False, code=self.code, error_code=response_can_purchase.error)

        response_purchase = store_service.purchase_item(user.id, cod_item)
        if not response_purchase.success:
            logger.error(f"Erro ao realizar a compra: {response_purchase.error}")
            return UseCaseResponse(success=False, code=self.code, error_code=response_purchase.error)

        logger.info(f"Compra realizada por {user.nome}: {response_purchase.data['item']} - {price} F₵")
        response_purchase.data["apelido"] = user.apelido
        return UseCaseResponse(
            success=True,
            code=self.code,
            data=response_purchase.data,
        )
