from loguru import logger

from domains.fabbank.services.transaction import TransactionService
from domains.fabzenda.repositories.user_animal import UserAnimalRepository
from domains.fabzenda.services.user_animal import UserAnimalService
from domains.user.repositories.user import UserRepository
from interfaces.presenters.hints import FabzendaHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class AlimentarAnimal:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.input.user_id)

        user_animal_repository = UserAnimalRepository(db)
        user_animal = user_animal_repository.get_user_animal_by_id(self.input.args[1])

        user_animal_service = UserAnimalService(db)

        # Verificando se o usuário pode e consegue alimentar o animal
        response_can_feed = user_animal_service._can_feed_animal_entity(user_id=user.id, user_animal=user_animal)

        if not response_can_feed.success:
            logger.error(f"[Alimentar Animal] Erro ao alimentar animal: {response_can_feed}")
            return UseCaseResponse(
                success=False,
                data={"apelido": user.apelido},
                notification=[
                    {"presenter_hint": response_can_feed.error},
                ],
            )

        # Removendo o dinheiro da conta do usuário
        transaction_service = TransactionService(db)
        response_transaction = transaction_service.change_coins(
            to_id=user.id,
            value=(-user_animal.feeding_cost),
            description=f"[Fabzenda] Alimentação Fabichinho: {user_animal.name}",
        )

        if not response_transaction.success:
            logger.error(f"[Alimentar Animal] Erro ao alimentar animal: {transaction_service}")
            return UseCaseResponse(
                success=False,
                data={"apelido": user.apelido},
                notification=[
                    {"presenter_hint": FabzendaHints.FEED_TRANSACTION_ERROR},
                ],
            )

        # Atualizar o status do animal alimentado
        service_response = user_animal_service._feed_animal_entity(user_animal=user_animal)

        if not service_response.success:
            logger.error(f"[Alimentar Animal] Erro ao alimentar animal: {service_response}")
            return UseCaseResponse(
                success=False,
                data={"apelido": user.apelido},
                notification=[
                    {"presenter_hint": service_response.error},
                ],
            )

        service_response.data["apelido"] = user.apelido
        logger.info(f"[Alimentar Animal] {service_response.data}")
        return UseCaseResponse(
            success=True,
            data=service_response.data,
            notification=[
                {"presenter_hint": FabzendaHints.FEED_SUCCESS},
            ],
        )
