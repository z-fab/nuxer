from domains.fabbank.repositories.wallet import WalletRepository
from domains.fabzenda.repositories.animal_type import AnimalTypeRepository
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
            return UseCaseResponse(success=False, notifications=[{"presenter_hint": "fabzenda.wallet_not_found"}])

        if not animal_types:
            return UseCaseResponse(success=False)

        return UseCaseResponse(
            success=True,
            data={
                "animal_types": animal_types,
                "balance": wallet.balance,
            },
            notification=[
                {"presenter_hint": "fabzenda.ver_celeiro"},
            ],
        )
