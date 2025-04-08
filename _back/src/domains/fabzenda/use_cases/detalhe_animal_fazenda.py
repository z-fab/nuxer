from domains.fabzenda.repositories.user_animal import UserAnimalRepository
from interfaces.presenters.hints import FabzendaHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class DetalheAnimalFazenda:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        user_animal_repository = UserAnimalRepository(db)
        user_animal = user_animal_repository.get_user_animal_by_id(self.input.args[1])

        if not user_animal:
            return UseCaseResponse(success=False)

        return UseCaseResponse(
            success=True,
            data={"user_animal": user_animal},
            notification=[
                {"presenter_hint": FabzendaHints.FAZENDA_OVERVIEW_DETALHE_ANIMAL},
            ],
        )
