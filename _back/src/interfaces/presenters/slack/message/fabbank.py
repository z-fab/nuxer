from datetime import datetime

from domains.fabbank import messages as MSG
from domains.fabbank.entities.wallet import WalletEntity


class FabbankSlackPresenter:
    def __init__(self, now: datetime | None = None):
        self.now = now or datetime.now()

    def balance(self, user_wallet: WalletEntity, **kwargs) -> str:
        return MSG.TEMPLATE_FABBANK_WALLET.format(
            apelido=user_wallet.user.apelido,
            balance=user_wallet.balance,
            id_wallet=user_wallet.wallet_id,
            data=self.now.strftime("%d/%m/%Y %H:%M:%S"),
        )

    def balance_admin(self, wallets: list[WalletEntity], total_balance: int, **kwargs) -> str:
        balances_text = ""
        for w in wallets:
            balances_text += f"*{w.user.nome}*: `F₵ {w.balance}`\n"

        return MSG.TEMPLATE_FABBANK_WALLET_ADMIN.format(balance_total=total_balance, balances=balances_text)

    def transfer_success(
        self, wallet_from: WalletEntity, wallet_to: WalletEntity, value: int, description: str, **kwargs
    ) -> str:
        return MSG.TEMPLATE_FABBANK_TRANSFER_SUCCESS.format(
            apelido=wallet_from.user.apelido,
            amount=value,
            to_name=wallet_to.user.nome,
            to_id_wallet=wallet_to.wallet_id,
            desc=description,
            id_wallet=wallet_from.wallet_id,
            data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        )

    def transfer_notification(
        self, wallet_from: WalletEntity, wallet_to: WalletEntity, value: int, description: str, **kwargs
    ) -> str:
        template = MSG.TEMPLATE_FABBANK_TRANSFER_RECEIVE if value > 0 else MSG.TEMPLATE_FABBANK_DISCOUNT_RECEIVE

        return template.format(
            to_apelido=wallet_to.user.apelido,
            amount=abs(value),
            from_name=wallet_from.user.nome,
            from_id_wallet=wallet_from.wallet_id,
            desc=description,
        )

    def wallet_not_found(self) -> str:
        return MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_WALLET_NOT_FOUND

    def wrong_params(self) -> str:
        return MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS

    def insufficient_balance(self) -> str:
        return MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_INSUFFICIENT_BALANCE

    def transfer_error(self) -> str:
        return MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS

    def transfer_permission(self) -> str:
        return MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_PERMISSION

    def generic_error(self) -> str:
        return "Ops, deu erro"
