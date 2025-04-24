from loguru import logger

from domains.fabbank.repositories.wallet import WalletRepository
from domains.fabzenda.repositories.animal_type import AnimalTypeRepository
from interfaces.presenters.hints import FabzendaHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class VerCeleiro:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        animal_type_repository = AnimalTypeRepository(db)
        animal_types = animal_type_repository.get_all_available()

        wallet_repository = WalletRepository(db)
        wallet = wallet_repository.get_wallet_by_slack_id(self.input.user_id)

        if not wallet:
            logger.error(f"[Ver Celeiro] Carteira não encontrada para o usuário: {self.input.user_id}")
            return UseCaseResponse(
                success=False, notifications=[{"presenter_hint": FabzendaHints.CELEIRO_WALLET_NOT_FOUND}]
            )

        if not animal_types:
            logger.error(f"[Ver Celeiro] Animais não encontrados para o usuário: {self.input.user_id}")
            return UseCaseResponse(success=False)

        logger.info(f"[Ver Celeiro] {animal_types}")
        return UseCaseResponse(
            success=True,
            data={
                "animal_types": animal_types,
                "balance": wallet.balance,
                "atual_page": int(self.input.args[1]) if len(self.input.args) > 1 else 1,
            },
            notification=[
                {"presenter_hint": FabzendaHints.CELEIRO_OVERVIEW},
            ],
        )
