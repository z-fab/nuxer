from datetime import datetime

from domains.fabbank import messages as MSG
from domains.fabbank.entities.item_loja import ItemLojaEntity


class FabbankSlackPresenter:
    def __init__(self, now: datetime | None = None):
        self.now = now or datetime.now()

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

        return "Vendinha do Uxer 🛍️", text

    def loja_buy_success(self, apelido: str, item: ItemLojaEntity, **kwargs) -> str:
        return "Compra Realizada 🛍️", MSG.LOJA_NOTIFICATION_BUY.format(
            apelido=apelido, item=f"[{item.cod}] {item.nome}", price=item.valor
        )

    def loja_buy_admin(self, apelido: str, item: ItemLojaEntity, **kwargs) -> str:
        return "", MSG.LOJA_NOTIFICATION_BUY_ADMIN.format(
            user_from=apelido,
            item=f"[{item.cod}] {item.nome}",
            price=item.valor,
            data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        )

    def loja_buy_error(self, apelido: str, item: ItemLojaEntity, **kwargs) -> str:
        return "Erro na Comprinha 🛍️", MSG.LOJA_BUY_ERROR.format(
            user_from=apelido, item=f"[{item.cod}] {item.nome}", price=item.valor
        )

    def loja_insufficient_balance(self, **kwargs) -> str:
        return "Erro na Comprinha 🛍️", MSG.LOJA_INSUFFICIENT_BALANCE

    def loja_item_price_changed(self, **kwargs) -> str:
        return "Erro na Comprinha 🛍️", MSG.LOJA_ITEM_PRICE_CHANGED

    def loja_item_unavailable(self, **kwargs) -> str:
        return "Erro na Comprinha 🛍️", MSG.LOJA_ITEM_UNAVAILABLE

    def loja_wallet_not_found(self, **kwargs) -> str:
        return "Erro na Comprinha 🛍️", MSG.LOJA_WALLET_NOT_FOUND
