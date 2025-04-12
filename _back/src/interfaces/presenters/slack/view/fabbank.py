from datetime import datetime

from domains.fabbank import messages as MSG
from domains.fabbank.entities.item_loja import ItemLojaEntity


class FabbankSlackPresenter:
    def __init__(self, now: datetime | None = None):
        self.now = now or datetime.now()

    def loja_buy_success(self, apelido: str, item: ItemLojaEntity, **kwargs) -> str:
        return "Minha Compra", MSG.LOJA_NOTIFICATION_BUY.format(
            apelido=apelido, item=f"[{item.cod}] {item.nome}", price=item.valor
        )

    def loja_buy_admin(self, apelido: str, item: ItemLojaEntity, **kwargs) -> str:
        return "Compra de Admin", MSG.LOJA_NOTIFICATION_BUY_ADMIN.format(
            user_from=apelido,
            item=f"[{item.cod}] {item.nome}",
            price=item.valor,
            data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        )

    # loja_buy_admin
    # loja_buy_error
    # loja_insufficient_balance
    # loja_item_price_changed
    # loja_item_unavailable
