from loguru import logger

from domains.fabzenda.repositories.animal_type import AnimalTypeRepository
from shared.dto.error_code import FabzendaError
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class DetalheAnimalCeleiro:
    def __init__(self, ucr: UseCaseRequest):
        self.user_id = ucr.payload.get("user_id", None)
        self.args = ucr.payload.get("args", None)
        self.code = ucr.code

    def __call__(self) -> UseCaseResponse:
        animal_type_repository = AnimalTypeRepository(db)
        animal_type = animal_type_repository.get_animal_type_by_id(self.args[1])

        if not animal_type:
            logger.error(f"[Detalhe Animal Celeiro] Tipo de animal não encontrado: {self.args[1]}")
            return UseCaseResponse(success=False, code=self.code, error_code=FabzendaError.GENERIC_ERROR)

        logger.info(f"[Detalhe Animal Celeiro] {animal_type}")
        return UseCaseResponse(
            success=True,
            code=self.code,
            data={"animal_type": animal_type},
        )
