from domains.fabbank.repositories.wallet import WalletRepository
from shared.dto.service_response import ServiceResponse


class WalletService:
    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repository: WalletRepository = wallet_repo

    def get_balance_info(self, slack_id: str) -> ServiceResponse:
        wallet = self.wallet_repository.get_wallet_by_slack_id(slack_id)

        if not wallet:
            return ServiceResponse(success=False, error="fabbank.wallet_not_found")

        if wallet.user.role == 0:
            return self._get_admin_balance()

        return ServiceResponse(
            success=True,
            data={"wallet": wallet},
        )

    def _get_admin_balance(self) -> ServiceResponse:
        all_wallets = self.wallet_repository.get_all_wallets()
        total_balance = sum(w.balance for w in all_wallets)

        return ServiceResponse(data={"wallets": all_wallets, "total_balance": total_balance}, success=True)
