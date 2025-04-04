from datetime import datetime

from domains.fabbank import messages as MSG
from domains.fabbank.entities.wallet import WalletEntity
from domains.fabbank.repositories.wallet import WalletRepository
from shared.dto.use_case_response import UseCaseResponse


class WalletService:
    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repository: WalletRepository = wallet_repo

    def get_balance_info(self, slack_id: str) -> UseCaseResponse:
        wallet = self.wallet_repository.get_wallet_by_slack_id(slack_id)

        if not wallet:
            return UseCaseResponse(message=MSG.TEMPLATE_FABBANK_WALLET_NOT_FOUND, success=False)

        if wallet.user.role == 0:
            return self._get_admin_balance()

        return self._get_user_balance(wallet)

    def _get_admin_balance(self) -> UseCaseResponse:
        all_wallets = self.wallet_repository.get_all_wallets()
        total_balance = sum(w.balance for w in all_wallets)

        balances_text = ""
        for w in all_wallets:
            balances_text += f"*{w.user.nome}*: `F₵ {w.balance}`\n"

        message = MSG.TEMPLATE_FABBANK_WALLET_ADMIN.format(balance_total=total_balance, balances=balances_text)

        return UseCaseResponse(message=message, success=True)

    def _get_user_balance(self, wallet: WalletEntity) -> UseCaseResponse:
        message = MSG.TEMPLATE_FABBANK_WALLET.format(
            id_wallet=wallet.wallet_id,
            balance=wallet.balance,
            apelido=wallet.user.apelido,
            data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        )

        return UseCaseResponse(message=message, success=True, data={"wallet": wallet})
