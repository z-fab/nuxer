from loguru import logger

from domains.fabbank.services.store import StoreService
from domains.user.repositories.user import UserRepository
from interfaces.presenters.hints import FabbankHints
from shared.config.const_slack import ID_USER_ADMIN
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class ComprarItem:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        store_service = StoreService(db)
        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.input.user_id)

        cod_item = self.input.args[1]
        price = int(self.input.args[2])

        response_can_purchase = store_service.can_purchase_item(user.id, cod_item, price)
        if not response_can_purchase.success:
            logger.error(f"Erro ao validar a compra: {response_can_purchase.error}")
            return UseCaseResponse(
                success=False,
                data={},
                notification=[
                    {"presenter_hint": response_can_purchase.error},
                ],
            )

        response_purchase = store_service.purchase_item(user.id, cod_item)
        if not response_purchase.success:
            logger.error(f"Erro ao realizar a compra: {response_purchase.error}")
            return UseCaseResponse(
                success=False,
                data={},
                notification=[
                    {"presenter_hint": response_purchase.error},
                ],
            )

        logger.info(f"Compra realizada por {user.nome}: {response_purchase.data['item']} - {price} F₵")
        user_admin = user_repository.get_user_by_slack_id(ID_USER_ADMIN)
        response_purchase.data["apelido"] = user.apelido
        return UseCaseResponse(
            success=True,
            data=response_purchase.data,
            notification=[
                {"presenter_hint": FabbankHints.LOJA_BUY_SUCCESS},
                {"presenter_hint": FabbankHints.LOJA_BUY_ADMIN, "user": user_admin},
            ],
        )
