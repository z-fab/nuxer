from domains.fabzenda.repositories.user_animal import UserAnimalRepository
from domains.fabzenda.services.user_animal import UserAnimalService
from domains.user.repositories.user import UserRepository
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class VerFabzenda:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        user_repository = UserRepository(db)
        user_entity = user_repository.get_user_by_slack_id(self.input.user_id)
        if not user_entity:
            return UseCaseResponse(success=False)

        user_animal_repository = UserAnimalRepository(db)
        user_animal_service = UserAnimalService(user_animal_repository, user_repository)

        response = user_animal_service.show_fabzenda(user_entity.id)

        return response
