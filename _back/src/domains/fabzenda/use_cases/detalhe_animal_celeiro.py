from domains.fabzenda.repositories.animal_type import AnimalTypeRepository
from interfaces.presenters.hints import FabzendaHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class DetalheAnimalCeleiro:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        animal_type_repository = AnimalTypeRepository(db)
        animal_type = animal_type_repository.get_animal_type_by_id(self.input.args[1])

        if not animal_type:
            return UseCaseResponse(success=False)

        return UseCaseResponse(
            success=True,
            data={"animal_type": animal_type},
            notification=[
                {"presenter_hint": FabzendaHints.CELEIRO_DETALHE_ANIMAL},
            ],
        )
