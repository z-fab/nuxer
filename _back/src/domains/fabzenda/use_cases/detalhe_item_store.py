from loguru import logger

from domains.fabzenda.repositories.item_definition import ItemDefinitionRepository
from shared.dto.error_code import FabzendaError
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class DetalheItemStore:
    def __init__(self, ucr: UseCaseRequest):
        self.user_id = ucr.payload.get("user_id", None)
        self.args = ucr.payload.get("args", None)
        self.code = ucr.code

    def __call__(self) -> UseCaseResponse:
        item_definition_repository = ItemDefinitionRepository(db)
        item = item_definition_repository.get_item_definition_by_id(self.args[1])

        if not item:
            logger.error(f"[Detalhe Item Store] Definição de Item não encontrado: {self.args[1]}")
            return UseCaseResponse(success=False, code=self.code, error_code=FabzendaError.GENERIC_ERROR)

        logger.info(f"[Detalhe Item Store] {item}")
        return UseCaseResponse(success=True, code=self.code, data={"item": item})
