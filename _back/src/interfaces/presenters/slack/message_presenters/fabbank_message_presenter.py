# interfaces/presenters/slack/message_presenters/fabbank_message_presenter.py
from datetime import datetime

from domains.fabbank.entities.wallet import WalletEntity
from shared.config.const_slack import ID_USER_ADMIN

from ..base_presenter import BaseSlackPresenter


class FabbankMessagePresenter(BaseSlackPresenter):
    ## Messages
    _GENERIC_ERROR = """
    Algo deu errado na minha comunicação com o Fabbank :warning:
    : Tente novamente mais tarde ou entre em contato com o Fabs
    """

    _LOJA_OPTIONS = """
    # Vendinha do Uxer 🛍️
    A melhor, maior e única loja do mundo que aceita Fabcoins! Preços atualizados a todo momento.
    : Clique no Botão abaixo para acessar
    .
    <🛍️ Entrar na Vendinha(fabbank)[opt=ver_loja]P>
    .
    """

    _BALANCE = """
    # Extrato do FabBank :moneybag:
    {apelido}, aqui está o saldo da sua Wallet:
    > *Saldo atual*: `F₵ {balance}`
    : Wallet ID: {id_wallet} - Valores atualizados em {data}
    """

    _BALANCE_ADMIN = """
    # Saldos no Fabbank
    Aqui estão os saldos no Fabbank
    > *Saldo Total*: `F₵ {balance_total}`
    --
    {balances}
    """

    _WALLET_NOT_FOUND = """
    Ops, parece que você não tem uma wallet no FabBank :warning:
    : Para criar uma fale com o Fabs
    """

    _TRANSFER_SUCCESS = """
    # Transferência Realizada com Sucesso :money_with_wings:
    {apelido}, você realizou uma transferência com o sucesso.
    > *Você transferiu* `F₵ {amount}` para `{to_name} (Wallet ID: {to_id_wallet})`
    *Motivo informado:* _{desc}_
    : Wallet ID: {id_wallet} - transação realizada em {data}
    """

    _TRANSFER_SUCCESS_NOTIFICATION_RECEIVE = """
    # Recebimento de Transferência :moneybag:
    {to_apelido}, você recebeu uma transferência em sua Wallet.
    > *Você recebeu* `F₵ {amount}` de `{from_name} (Wallet ID: {from_id_wallet})`
    *Motivo informado:* _{desc}_
    """

    _TRANSFER_WALLET_NOT_FOUND = """
    Ops, parece que você (ou a pessoa para quem você quer transferir) não tem uma wallet no FabBank :warning:
    : Para criar uma, fale com o Fabs
    """

    _TRANSFER_WRONG_PARAMS = """
    Ops, parece que você não preencheu corretamente os parâmetros para realizar a transferência :warning:
    : Para realizar a transferência, utilize o comando `!fb` `pix` `[@usuario]` `[valor]` `"[descrição]"`
    """

    _TRANSFER_INSUFFICIENT_BALANCE = """
    Ops, parece que você não tem saldo suficiente para realizar a transferência ou o valor informado é inválido :warning:
    : Verifique o saldo da sua Wallet com o comando `!fb` `saldo`
    """

    _TRANSFER_SUCCESS_NOTIFICATION_DISCOUNT = """
    # Desconto Aplicado :money_with_wings:
    {to_apelido}, você recebeu um desconto em sua Wallet.
    > *Você foi descontado* em `F₵ {amount}` pelo `{from_name} (Wallet ID: {from_id_wallet})`
    *Motivo informado:* _{desc}_
    """

    _TRANSFER_DONT_HAVE_PERMISSION = """
    Ops, você não tem permissão para realizar essa transferência :warning:
    : Como você descobriu esse comando? :eyes:
    """

    _LOJA_OVERVIEW = """
    A melhor, maior e única loja do mundo que aceita Fabcoins! Preços atualizados a todo momento.
    > Seu saldo: `F₵ {balance}`
    --
    .
    {items}
    """

    _LOJA_OVERVIEW_ITEM = """
    [ cod: *{id}* ] {item} `F₵ {price}`
    : {description}
    {amount}
    <🛒 Comprar(fabbank)[opt=comprar,id={id},preco={price}]P>
    .
    --
    .
    """

    _LOJA_NOTIFICATION_BUY = """
    {apelido}, você comprou um item da loja com sucesso!
    > {item} por `F₵ {price}`
    : Já notifiquei o fabs e em breve o item será enviado.
    """

    _LOJA_NOTIFICATION_BUY_ADMIN = """
    --
    # Item Comprado 🛍️
    {user_from} comprou um item da loja.
    > {item} por `F₵ {price}` em {data}
    --
    """

    _LOJA_BUY_ERROR = """
    {apelido}, não foi possível realizar a compra do seu item. Verifique seu saldo ou se o preço do item não foi alterado
    > {item} por `F₵ {price}`
    : Para verificar seu saldo, utilize o comando `!fb` `saldo` e para verificar os itens com preço atualizado, utilize o comando `!fb` `loja`
    """

    _LOJA_INSUFFICIENT_BALANCE = """
    Ops, parece que você não tem saldo suficiente para realizar a compra :warning:
    : Verifique o saldo da sua Wallet com o comando `!fb` `saldo`
    """

    _LOJA_ITEM_PRICE_CHANGED = """
    Ops, parece que o preço do item que você tentou comprar foi alterado :warning:
    : Verifique os preços atualizados com o comando `!fb` `loja`
    """

    _LOJA_ITEM_UNAVAILABLE = """
    Ops, parece que o item que você tentou comprar não está mais disponível :warning:
    : Verifique os itens disponíveis com o comando `!fb` `loja`
    """

    _LOJA_WALLET_NOT_FOUND = """
    Ops, parece que você não tem uma wallet no FabBank. Você precisa de uma para comprar na loja :warning:
    : Para criar uma wallet fale com o Fabs
    """

    TEMPLATE_FABBANK_EXTRACT = """
    # Extrato FabBank :moneybag:
    {apelido}, aqui está o extrato da sua Wallet (ID {id_wallet}) em {data}:
    > *Saldo atual*: `F₵ {balance}`
    --
    {extract}
    """

    TEMPLATE_FABBANK_EXTRACT_TRANSACTION = """
    *{user_from}* (Wallet ID: {id_wallet_from}) transferiu `F₵ {amount}`
    *Motivo:* {description}
    : Transação realizada em {timestamp}
    --
    """

    ## Success Messages

    def option_loja(self, data: dict):
        return self._say(self._LOJA_OPTIONS)

    def consultar_saldo_sucesso(self, data: dict):
        user_wallet: WalletEntity = data.get("user_wallet")

        if data.get("wallets"):
            balances_text = ""
            for w in data["wallets"]:
                balances_text += f"*{w.user.nome}*: `F₵ {w.balance}`\n"

            message_text = self._BALANCE_ADMIN.format(
                balance_total=data.get("total_balance", 0), balances=balances_text
            )
        else:
            message_text = self._BALANCE.format(
                apelido=user_wallet.user.apelido,
                balance=user_wallet.balance,
                id_wallet=user_wallet.wallet_id,
                data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )

        self._say(message_text)

    def consultar_saldo_sucesso_dm(self, data: dict):
        user_wallet: WalletEntity = data.get("user_wallet")

        if data.get("wallets"):
            balances_text = ""
            for w in data["wallets"]:
                balances_text += f"*{w.user.nome}*: `F₵ {w.balance}`\n"

            message_text = self._BALANCE_ADMIN.format(
                balance_total=data.get("total_balance", 0), balances=balances_text
            )
        else:
            message_text = self._BALANCE.format(
                apelido=user_wallet.user.apelido,
                balance=user_wallet.balance,
                id_wallet=user_wallet.wallet_id,
                data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )

        self._send_dm_to_user(self._get_user_id(), message_text)

    def transferir_sucesso(self, data: dict):
        wallet_from: WalletEntity = data.get("wallet_from")
        wallet_to: WalletEntity = data.get("wallet_to")

        message_text = self._TRANSFER_SUCCESS.format(
            apelido=wallet_from.user.apelido,
            amount=data.get("value"),
            to_name=wallet_to.user.nome,
            to_id_wallet=wallet_to.wallet_id,
            desc=data.get("description"),
            id_wallet=wallet_from.wallet_id,
            data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        )
        self._say(message_text)

        value = data.get("value")
        template_message = self._TRANSFER_SUCCESS_NOTIFICATION_RECEIVE
        if data.get("value") < 0:
            value = abs(int(data.get("value")))
            template_message = self._TRANSFER_SUCCESS_NOTIFICATION_DISCOUNT

        # Notificação para o destinatário
        message_text_to = template_message.format(
            to_apelido=wallet_to.user.apelido,
            amount=value,
            from_name=wallet_from.user.nome,
            from_id_wallet=wallet_from.wallet_id,
            desc=data.get("description"),
        )

        self._send_dm_to_user(user_id=wallet_to.user.slack_id, message=message_text_to)

    def ver_loja_sucesso(self, data: dict):
        items = ""
        for item in data.get("all_items", []):
            items += self._LOJA_OVERVIEW_ITEM.format(
                id=item.cod,
                item=item.nome,
                price=item.valor,
                description=item.descricao,
                amount=f"Quantidade disponível: {item.amount}"
                if item.amount > 0
                else "Esgotado"
                if item.amount == 0
                else "",
            )

        message_text = self._LOJA_OVERVIEW.format(
            balance=data.get("balance", 0),
            items=items,
        )

        self._say(message_text)

    ## Success View
    def view_ver_loja_sucesso(self, data: dict):
        items = ""
        for item in data.get("all_items", []):
            items += self._LOJA_OVERVIEW_ITEM.format(
                id=item.cod,
                item=item.nome,
                price=item.valor,
                description=item.descricao,
                amount=f"Quantidade disponível: {item.amount}"
                if item.amount > 0
                else "Esgotado"
                if item.amount == 0
                else "",
            )

        message_text = self._LOJA_OVERVIEW.format(
            balance=data.get("balance", 0),
            items=items,
        )

        self._set_view(
            content=message_text,
            title="Loja do Fabbank",
        )

    def view_comprar_item_sucesso(self, data: dict):
        item = data.get("item")

        message_text = self._LOJA_NOTIFICATION_BUY.format(
            apelido=data.get("apelido"),
            item=item.nome,
            price=item.valor,
        )

        self._set_view(
            content=message_text,
            title="Compra Realizada",
        )

        # Notificação para o admin
        message_text_admin = self._LOJA_NOTIFICATION_BUY_ADMIN.format(
            user_from=data.get("apelido"),
            item=item.nome,
            price=item.valor,
            data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        )
        self._send_dm_to_user(user_id=ID_USER_ADMIN, message=message_text_admin)

    ## Error Messages

    def error_generic(self, data: dict):
        self._say(self._GENERIC_ERROR)

    def error_wallet_not_found(self, data: dict):
        self._say(self._WALLET_NOT_FOUND)

    def error_transfer_wallet_not_found(self, data: dict):
        self._say(self._TRANSFER_WALLET_NOT_FOUND)

    def error_insufficient_balance(self, data: dict):
        self._say(self._TRANSFER_INSUFFICIENT_BALANCE)

    def error_wrong_params(self, data: dict):
        self._say(self._TRANSFER_WRONG_PARAMS)

    def error_transfer_dont_have_permission(self, data: dict):
        self._say(self._TRANSFER_DONT_HAVE_PERMISSION)

    def error_loja_wallet_not_found(self, data: dict):
        self._set_view(title="Ops!", content=self._LOJA_WALLET_NOT_FOUND)

    def error_loja_item_unavailable(self, data: dict):
        self._set_view(title="Ops!", content=self._LOJA_ITEM_UNAVAILABLE)

    def error_loja_insufficient_balance(self, data: dict):
        self._set_view(title="Ops!", content=self._LOJA_INSUFFICIENT_BALANCE)

    def error_loja_item_price_changed(self, data: dict):
        self._set_view(title="Ops!", content=self._LOJA_ITEM_PRICE_CHANGED)
