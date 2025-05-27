from loguru import logger

from domains.fabbank.services.transaction import TransactionService
from domains.fabzenda.repositories.user_animal import UserAnimalRepository
from domains.fabzenda.services.user_animal import UserAnimalService
from domains.user.repositories.user import UserRepository
from shared.dto.error_code import FabzendaError
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class AlimentarAnimal:
    def __init__(self, ucr: UseCaseRequest):
        self.user_id = ucr.payload.get("user_id", None)
        self.args = ucr.payload.get("args", None)
        self.code = ucr.code

    def __call__(self) -> UseCaseResponse:
        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.user_id)

        user_animal_repository = UserAnimalRepository(db)
        user_animal = user_animal_repository.get_user_animal_by_id(self.args[1])

        user_animal_service = UserAnimalService(db)

        # Verificando se o usuário pode e consegue alimentar o animal
        response_can_feed = user_animal_service._can_feed_animal_entity(user_id=user.id, user_animal=user_animal)

        if not response_can_feed.success:
            logger.error(f"[Alimentar Animal] Erro ao alimentar animal: {response_can_feed}")
            return UseCaseResponse(
                success=False, code=self.code, error_code=response_can_feed.error, data={"apelido": user.apelido}
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
                code=self.code,
                error_code=FabzendaError.FEED_TRANSACTION_ERROR,
                data={"apelido": user.apelido},
            )

        # Atualizar o status do animal alimentado
        service_response = user_animal_service._feed_animal_entity(user_animal=user_animal)

        if not service_response.success:
            logger.error(f"[Alimentar Animal] Erro ao alimentar animal: {service_response}")
            return UseCaseResponse(
                success=False, code=self.code, error_code=service_response.error, data={"apelido": user.apelido}
            )

        service_response.data["apelido"] = user.apelido
        logger.info(f"[Alimentar Animal] {service_response.data}")
        return UseCaseResponse(success=True, code=self.code, data=service_response.data)
