from loguru import logger

from domains.fabbank.services.transaction import TransactionService
from domains.fabzenda.repositories.animal_type import AnimalTypeRepository
from domains.fabzenda.services.user_animal import UserAnimalService
from domains.user.repositories.user import UserRepository
from shared.dto.error_code import FabzendaError
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class ComprarAnimal:
    def __init__(self, ucr: UseCaseRequest):
        self.user_id = ucr.payload.get("user_id", None)
        self.args = ucr.payload.get("args", None)
        self.code = ucr.code

    def __call__(self) -> UseCaseResponse:
        user_repository = UserRepository(db)
        user = user_repository.get_user_by_slack_id(self.user_id)

        animal_type_repository = AnimalTypeRepository(db)
        animal_type = animal_type_repository.get_animal_type_by_id(self.args[1])

        user_animal_service = UserAnimalService(db)

        # Verificando se o usuário pode e consegue comprar o animal
        response_can_buy = user_animal_service._can_buy_animal_entity(user_id=user.id, animal_type=animal_type)

        if not response_can_buy.success:
            logger.error(f"[Comprar Animal] Erro ao comprar animal: {response_can_buy}")
            return UseCaseResponse(
                success=False,
                code=self.code,
                data={"apelido": user.apelido},
                error_code=response_can_buy.error,
            )

        # Removendo o dinheiro da conta do usuário
        transaction_service = TransactionService(db)
        response_transaction = transaction_service.change_coins(
            to_id=user.id,
            value=(-animal_type.base_price),
            description=f"[Fabzenda] Adoção Fabichinho: {animal_type.name}",
        )

        if not response_transaction.success:
            logger.error(f"[Comprar Animal] Erro ao comprar animal: {transaction_service}")
            return UseCaseResponse(
                success=False,
                code=self.code,
                data={"apelido": user.apelido},
                error_code=FabzendaError.CELEIRO_TRANSACTION_ERROR,
            )

        service_response = user_animal_service._buy_animal_entity(
            user_id=user.id,
            animal_type=animal_type,
        )

        if not service_response.success:
            logger.error(f"[Comprar Animal] Erro ao comprar animal: {service_response}")
            return UseCaseResponse(
                success=False,
                code=self.code,
                data={"apelido": user.apelido},
                error_code=service_response.error,
            )

        service_response.data["user"] = user
        logger.info(f"[Comprar Animal] {service_response.data}")
        return UseCaseResponse(success=True, code=self.code, data=service_response.data)
