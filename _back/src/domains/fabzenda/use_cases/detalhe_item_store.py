from loguru import logger

from domains.fabzenda.repositories.item_definition import ItemDefinitionRepository
from interfaces.presenters.hints import FabzendaHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class DetalheItemStore:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        item_definition_repository = ItemDefinitionRepository(db)
        item = item_definition_repository.get_item_definition_by_id(self.input.args[1])

        if not item:
            logger.error(f"[Detalhe Item Store] Definição de Item não encontrado: {self.input.args[1]}")
            return UseCaseResponse(success=False)

        logger.info(f"[Detalhe Item Store] {item}")
        return UseCaseResponse(
            success=True,
            data={"item": item},
            notification=[
                {"presenter_hint": FabzendaHints.STORE_DETALHE_ITEM},
            ],
        )
