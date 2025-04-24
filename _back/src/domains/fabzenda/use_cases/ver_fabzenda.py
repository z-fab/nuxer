from loguru import logger

from domains.fabzenda.services.item import ItemService
from domains.fabzenda.services.user_animal import UserAnimalService
from domains.user.repositories.user import UserRepository
from interfaces.presenters.hints import FabzendaHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class VerFabzenda:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        user_repository = UserRepository(db)
        user_entity = user_repository.get_user_by_slack_id(self.input.user_id)

        item_service = ItemService(db)
        qtd_additional = item_service.get_additional_animals_slot_by_user(user_entity.id)

        if not user_entity:
            logger.error(f"[Ver Fabzenda] Usuário não encontrado: {self.input.user_id}")
            return UseCaseResponse(success=False)

        user_animal_service = UserAnimalService(db)

        response = user_animal_service.get_user_animals(user_entity.id)

        if not response.success:
            logger.error(f"[Ver Fabzenda] Erro ao buscar animais do usuário: {response}")
            return UseCaseResponse(
                success=False,
                data=response.data,
                notification=[
                    {"presenter_hint": response.error},
                ],
            )

        response.data["qtd_additional"] = qtd_additional.data["n_animals"]
        logger.info(f"[Ver Fabzenda] {response.data}")
        return UseCaseResponse(
            success=True,
            data=response.data,
            notification=[
                {"presenter_hint": FabzendaHints.FAZENDA_OVERVIEW},
            ],
        )
