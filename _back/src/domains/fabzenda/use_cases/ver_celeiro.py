from loguru import logger

from domains.fabbank.repositories.wallet import WalletRepository
from domains.fabzenda.repositories.animal_type import AnimalTypeRepository
from shared.dto.error_code import FabzendaError
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class VerCeleiro:
    def __init__(self, ucr: UseCaseRequest):
        self.user_id = ucr.payload.get("user_id", None)
        self.args = ucr.payload.get("args", None)
        self.code = ucr.code

    def __call__(self) -> UseCaseResponse:
        animal_type_repository = AnimalTypeRepository(db)
        animal_types = animal_type_repository.get_all_available()

        wallet_repository = WalletRepository(db)
        wallet = wallet_repository.get_wallet_by_slack_id(self.user_id)

        if not wallet:
            logger.error(f"[Ver Celeiro] Carteira não encontrada para o usuário: {self.user_id}")
            return UseCaseResponse(success=False, code=self.code, error_code=FabzendaError.WALLET_NOT_FOUND)

        if not animal_types:
            logger.error(f"[Ver Celeiro] Animais não encontrados para o usuário: {self.user_id}")
            return UseCaseResponse(success=False, code=self.code, error_code=FabzendaError.GENERIC_ERROR)

        logger.info(f"[Ver Celeiro] {animal_types}")
        return UseCaseResponse(
            success=True,
            code=self.code,
            data={
                "animal_types": animal_types,
                "balance": wallet.balance,
                "atual_page": int(self.args[1]) if (1 in self.args) else 1,
            },
        )
