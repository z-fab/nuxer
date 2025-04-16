from domains.fabbank.services.transaction import TransactionService
from domains.fabzenda.repositories.animal_type import AnimalTypeRepository
from domains.fabzenda.services.user_animal import UserAnimalService
from domains.user.repositories.user import UserRepository
from interfaces.presenters.hints import FabzendaHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class ComprarAnimal:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.input.user_id)

        animal_type_repository = AnimalTypeRepository(db)
        animal_type = animal_type_repository.get_animal_type_by_id(self.input.args[1])

        user_animal_service = UserAnimalService(db)

        # Verificando se o usuário pode e consegue comprar o animal
        response_can_buy = user_animal_service._can_buy_animal_entity(user_id=user.id, animal_type=animal_type)

        if not response_can_buy.success:
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
            value=(-animal_type.base_price),
            description=f"[Fabzenda] Adoção Fabichinho: {animal_type.name}",
        )

        if not response_transaction.success:
            return UseCaseResponse(
                success=False,
                data={"apelido": user.apelido},
                notification=[
                    {"presenter_hint": FabzendaHints.CELEIRO_TRANSACTION_ERROR},
                ],
            )

        service_response = user_animal_service._buy_animal_entity(
            user_id=user.id,
            animal_type=animal_type,
        )

        if not service_response.success:
            return UseCaseResponse(
                success=False,
                data={"apelido": user.apelido},
                notification=[
                    {"presenter_hint": service_response.error},
                ],
            )

        service_response.data["user"] = user
        return UseCaseResponse(
            success=True,
            data=service_response.data,
            notification=[
                {"presenter_hint": FabzendaHints.CELEIRO_ANIMAL_BUY_SUCCESS},
            ],
        )
