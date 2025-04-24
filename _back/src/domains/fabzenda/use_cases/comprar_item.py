from loguru import logger

from domains.fabbank.services.transaction import TransactionService
from domains.fabzenda.repositories.item_definition import ItemDefinitionRepository
from domains.fabzenda.services.item import ItemService
from domains.user.repositories.user import UserRepository
from interfaces.presenters.hints import FabzendaHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class ComprarItem:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.input.user_id)

        item_definition_repository = ItemDefinitionRepository(db)
        item = item_definition_repository.get_item_definition_by_id(self.input.args[1])

        item_service = ItemService(db)

        # Verificando se o usuário pode e consegue comprar o animal
        response_can_buy = item_service._can_buy_item_entity(user_id=user.id, item=item)

        if not response_can_buy.success:
            logger.error(f"[Comprar Item] Erro ao comprar item: {response_can_buy}")
            return UseCaseResponse(
                success=False,
                data={"apelido": user.apelido},
                notification=[
                    {"presenter_hint": response_can_buy.error},
                ],
            )

        # Removendo o dinheiro da conta do usuário
        transaction_service = TransactionService(db)
        response_transaction = transaction_service.change_coins(
            to_id=user.id,
            value=(-item.price),
            description=f"[Fabzenda] Compra de Item: {item.name}",
        )

        if not response_transaction.success:
            logger.error(f"[Comprar Item] Erro ao comprar item: {transaction_service}")
            return UseCaseResponse(
                success=False,
                data={"apelido": user.apelido},
                notification=[
                    {"presenter_hint": FabzendaHints.STORE_TRANSACTION_ERROR},
                ],
            )

        service_response = item_service._buy_item_entity(
            user_id=user.id,
            item=item,
        )

        if not service_response.success:
            logger.error(f"[Comprar Item] Erro ao comprar o item: {service_response}")
            return UseCaseResponse(
                success=False,
                data={"apelido": user.apelido},
                notification=[
                    {"presenter_hint": service_response.error},
                ],
            )

        service_response.data["apelido"] = user.apelido
        logger.info(f"[Comprar Item] {service_response.data}")
        return UseCaseResponse(
            success=True,
            data=service_response.data,
            notification=[
                {"presenter_hint": FabzendaHints.STORE_BUY_SUCCESS},
            ],
        )
