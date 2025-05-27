from loguru import logger

from domains.fabzenda.repositories.user_animal import UserAnimalRepository
from shared.dto.error_code import FabzendaError
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class DetalheAnimalFazenda:
    def __init__(self, ucr: UseCaseRequest):
        self.user_id = ucr.payload.get("user_id", None)
        self.args = ucr.payload.get("args", None)
        self.code = ucr.code

    def __call__(self) -> UseCaseResponse:
        user_animal_repository = UserAnimalRepository(db)
        user_animal = user_animal_repository.get_user_animal_by_id(self.args[1])

        if not user_animal:
            logger.error(f"[Detalhe Animal] Animal não encontrado: {self.args[1]}")
            return UseCaseResponse(success=False, code=self.code, error_code=FabzendaError.GENERIC_ERROR)

        logger.info(f"[Detalhe Animal] {user_animal}")
        return UseCaseResponse(success=True, data={"user_animal": user_animal}, code=self.code)
