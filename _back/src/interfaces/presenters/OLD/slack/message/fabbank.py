from datetime import datetime

from domains.fabbank import messages as MSG
from domains.fabbank.entities.item_loja import ItemLojaEntity
from domains.fabbank.entities.wallet import WalletEntity


class FabbankSlackPresenter:
    def __init__(self, now: datetime | None = None):
        self.now = now or datetime.now()

    def balance(self, user_wallet: WalletEntity, **kwargs) -> str:
        return MSG.BALANCE.format(
            apelido=user_wallet.user.apelido,
            balance=user_wallet.balance,
            id_wallet=user_wallet.wallet_id,
            data=self.now.strftime("%d/%m/%Y %H:%M:%S"),
        )

    def balance_admin(self, wallets: list[WalletEntity], total_balance: int, **kwargs) -> str:
        balances_text = ""
        for w in wallets:
            balances_text += f"*{w.user.nome}*: `F₵ {w.balance}`\n"

        return MSG.BALANCE_ADMIN.format(balance_total=total_balance, balances=balances_text)

    def balance_wallet_not_found(self) -> str:
        return MSG.BALANCE_WALLET_NOT_FOUND

    ##
    def transfer_success(
        self, wallet_from: WalletEntity, wallet_to: WalletEntity, value: int, description: str, **kwargs
    ) -> str:
        return MSG.TRANSFER_SUCCESS.format(
            apelido=wallet_from.user.apelido,
            amount=value,
            to_name=wallet_to.user.nome,
            to_id_wallet=wallet_to.wallet_id,
            desc=description,
            id_wallet=wallet_from.wallet_id,
            data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        )

    def transfer_success_notification(
        self, wallet_from: WalletEntity, wallet_to: WalletEntity, value: int, description: str, **kwargs
    ) -> str:
        template = (
            MSG.TRANSFER_SUCCESS_NOTIFICATION_RECEIVE if value > 0 else MSG.TRANSFER_SUCCESS_NOTIFICATION_DISCOUNT
        )

        return template.format(
            to_apelido=wallet_to.user.apelido,
            amount=abs(value),
            from_name=wallet_from.user.nome,
            from_id_wallet=wallet_from.wallet_id,
            desc=description,
        )

    def transfer_wrong_params(self) -> str:
        return MSG.TRANSFER_WRONG_PARAMS

    def transfer_insufficient_balance(self) -> str:
        return MSG.TRANSFER_INSUFFICIENT_BALANCE

    def transfer_error(self) -> str:
        return MSG.TRANSFER_WRONG_PARAMS

    def transfer_permission(self) -> str:
        return MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_PERMISSION

    ##

    def loja_options(self, **kwargs) -> str:
        return MSG.LOJA_OPTIONS

    def loja_overview(self, all_items: list[ItemLojaEntity], balance: int, **kwargs) -> str:
        items = ""
        for item in all_items:
            if item.amount > 0 or item.amount == -1:
                preco_item = item.valor

                items += MSG.LOJA_OVERVIEW_ITEM.format(
                    id=item.cod,
                    item=item.nome,
                    price=preco_item,
                    description=item.descricao,
                    amount=f": Quantidade Disponível: {item.amount}" if item.amount > 0 else "",
                )

        text = MSG.LOJA_OVERVIEW.format(
            balance=balance,
            items=items,
        )

        return text

    def loja_wallet_not_found(self, **kwargs) -> str:
        return MSG.LOJA_WALLET_NOT_FOUND
