from loguru import logger

from domains.fabbank.repositories.wallet import WalletRepository
from domains.fabzenda.repositories.item_definition import ItemDefinitionRepository
from interfaces.presenters.hints import FabzendaHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class VerStore:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        item_definition_repository = ItemDefinitionRepository(db)
        items = item_definition_repository.get_all_available()

        wallet_repository = WalletRepository(db)
        wallet = wallet_repository.get_wallet_by_slack_id(self.input.user_id)

        if not wallet:
            logger.error(f"[Ver Store] Carteira não encontrada para o usuário: {self.input.user_id}")
            return UseCaseResponse(
                success=False, notifications=[{"presenter_hint": FabzendaHints.STORE_WALLET_NOT_FOUND}]
            )

        if not items:
            logger.error(f"[Ver Store] Animais não encontrados para o usuário: {self.input.user_id}")
            return UseCaseResponse(success=False)

        logger.info(f"[Ver Store] {items}")
        return UseCaseResponse(
            success=True,
            data={
                "items": items,
                "balance": wallet.balance,
                "atual_page": int(self.input.args[1]) if len(self.input.args) > 1 else 1,
            },
            notification=[
                {"presenter_hint": FabzendaHints.STORE_OVERVIEW},
            ],
        )
