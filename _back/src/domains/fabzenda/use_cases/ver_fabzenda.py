from loguru import logger

from domains.fabzenda.services.item import ItemService
from domains.fabzenda.services.user_animal import UserAnimalService
from domains.user.repositories.user import UserRepository
from shared.dto.error_code import FabzendaError
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class VerFabzenda:
    def __init__(self, ucr: UseCaseRequest):
        self.user_id = ucr.payload.get("user_id", None)
        self.args = ucr.payload.get("args", None)
        self.code = ucr.code

    def __call__(self) -> UseCaseResponse:
        user_repository = UserRepository(db)
        user_entity = user_repository.get_user_by_slack_id(self.user_id)

        item_service = ItemService(db)
        qtd_additional = item_service.get_additional_animals_slot_by_user(user_entity.id)

        if not user_entity:
            logger.error(f"[Ver Fabzenda] Usuário não encontrado: {self.user_id}")
            return UseCaseResponse(success=False, code=self.code, error_code=FabzendaError.GENERIC_ERROR)

        user_animal_service = UserAnimalService(db)

        response = user_animal_service.get_user_animals(user_entity.id)

        if not response.success:
            logger.error(f"[Ver Fabzenda] Erro ao buscar animais do usuário: {response}")
            return UseCaseResponse(success=False, code=self.code, data=response.data, error_code=response.error)

        response.data["qtd_additional"] = qtd_additional.data["n_animals"]
        logger.info(f"[Ver Fabzenda] {response.data}")
        return UseCaseResponse(success=True, code=self.code, data=response.data)
