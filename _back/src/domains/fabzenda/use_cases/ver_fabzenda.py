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

        user_animal_service = UserAnimalService(db)

        response = user_animal_service.get_user_animals(user_entity.id)

        if response.success:
            return UseCaseResponse(
                success=True,
                data=response.data,
                notification=[
                    {"presenter_hint": "fabzenda.ver_fazenda"},
                ],
            )

        return response
