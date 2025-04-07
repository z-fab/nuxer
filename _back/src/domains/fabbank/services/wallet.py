from domains.fabbank.repositories.wallet import WalletRepository
from shared.dto.service_response import ServiceResponse
from shared.infrastructure.db_context import DatabaseExternal


class WalletService:
    def __init__(self, db_context: DatabaseExternal):
        self.wallet_repository = WalletRepository(db_context)

    def get_balance_info(self, user_id: str) -> ServiceResponse:
        wallet = self.wallet_repository.get_wallet_by_user_id(user_id)

        if not wallet:
            return ServiceResponse(success=False, error="fabbank.wallet_not_found")

        if wallet.user.role == 0:
            response = self._get_admin_balance()
            response.data["user_wallet"] = wallet
            return response

        return ServiceResponse(
            success=True,
            data={"user_wallet": wallet},
        )

    def _get_admin_balance(self) -> ServiceResponse:
        all_wallets = self.wallet_repository.get_all_wallets()
        total_balance = sum(w.balance for w in all_wallets)

        return ServiceResponse(data={"wallets": all_wallets, "total_balance": total_balance}, success=True)
