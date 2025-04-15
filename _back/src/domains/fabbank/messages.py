TEMPLATE_FABBANK_WALLET_NOT_FOUND = """
Ops, parece que você não tem uma wallet no FabBank :warning:
: Para criar uma fale com o Fabs
"""

### FABBANK BALANCE ###

BALANCE = """
# Extrato do FabBank :moneybag:
{apelido}, aqui está o saldo da sua Wallet:
> *Saldo atual*: `F₵ {balance}`
: Wallet ID: {id_wallet} - Valores atualizados em {data}
"""

BALANCE_ADMIN = """
# Saldos no Fabbank
Aqui estão os saldos no Fabbank
> *Saldo Total*: `F₵ {balance_total}`
--
{balances}
"""

BALANCE_WALLET_NOT_FOUND = """
Ops, parece que você não tem uma wallet no FabBank :warning:
: Para criar uma fale com o Fabs
"""


### FABBANK TRANSFERÊNCIA ###

TRANSFER_SUCCESS = """
# Transferência Realizada com Sucesso :money_with_wings:
{apelido}, você realizou uma transferência com o sucesso.
> *Você transferiu* `F₵ {amount}` para `{to_name} (Wallet ID: {to_id_wallet})`
*Motivo informado:* _{desc}_
: Wallet ID: {id_wallet} - transação realizada em {data}
"""

TRANSFER_SUCCESS_NOTIFICATION_RECEIVE = """
# Recebimento de Transferência :moneybag:
{to_apelido}, você recebeu uma transferência em sua Wallet.
> *Você recebeu* `F₵ {amount}` de `{from_name} (Wallet ID: {from_id_wallet})`
*Motivo informado:* _{desc}_
"""

TRANSFER_SUCCESS_NOTIFICATION_DISCOUNT = """
# Desconto Aplicado :money_with_wings:
{to_apelido}, você recebeu um desconto em sua Wallet.
> *Você foi descontado* em `F₵ {amount}` pelo `{from_name} (Wallet ID: {from_id_wallet})`
*Motivo informado:* _{desc}_
"""

TRANSFER_ERROR = """
Ops, ocorreu um erro ao realizar a transferência :warning:
: Tente novamente, e caso não funcione, avise o Fabs
"""

TRANSFER_WALLET_NOT_FOUND = """
Ops, parece que você (ou a pessoa para quem você quer transferir) não tem uma wallet no FabBank :warning:
: Para criar uma, fale com o Fabs
"""

TRANSFER_WRONG_PARAMS = """
Ops, parece que você não preencheu corretamente os parâmetros para realizar a transferência :warning:
: Para realizar a transferência, utilize o comando `!fb` `pix` `[@usuario]` `[valor]` `"[descrição]"`
"""

TRANSFER_INSUFFICIENT_BALANCE = """
Ops, parece que você não tem saldo suficiente para realizar a transferência ou o valor informado é inválido :warning:
: Verifique o saldo da sua Wallet com o comando `!fb` `saldo`
"""

TRANSFER_DONT_HAVE_PERMISSION = """
Ops, você não tem permissão para realizar essa transferência :warning:
: Como você descobriu esse comando? :eyes:
"""


### FABBANK LOJA ###

LOJA_OPTIONS = """
# Vendinha do Uxer 🛍️
A melhor, maior e única loja do mundo que aceita Fabcoins! Preços atualizados a todo momento.
: Clique no Botão abaixo para acessar
.
<🛍️ Entrar na Vendinha(fabbank)[opt=ver_loja]P>
.
"""

LOJA_OVERVIEW = """
A melhor, maior e única loja do mundo que aceita Fabcoins! Preços atualizados a todo momento.
> Seu saldo: `F₵ {balance}`
--
.
{items}
"""

LOJA_OVERVIEW_ITEM = """
[ cod: *{id}* ] {item} `F₵ {price}`
: {description}
{amount}
<🛒 Comprar(fabbank)[opt=comprar,id={id},preco={price}]P>
.
--
.
"""

LOJA_NOTIFICATION_BUY = """
{apelido}, você comprou um item da loja com sucesso!
> {item} por `F₵ {price}`
: Já notifiquei o fabs e em breve o item será enviado.
"""

LOJA_NOTIFICATION_BUY_ADMIN = """
--
# Item Comprado 🛍️
{user_from} comprou um item da loja.
> {item} por `F₵ {price}` em {data}
--
"""

LOJA_BUY_ERROR = """
{apelido}, não foi possível realizar a compra do seu item. Verifique seu saldo ou se o preço do item não foi alterado
> {item} por `F₵ {price}`
: Para verificar seu saldo, utilize o comando `!fb` `saldo` e para verificar os itens com preço atualizado, utilize o comando `!fb` `loja`
"""

LOJA_INSUFFICIENT_BALANCE = """
Ops, parece que você não tem saldo suficiente para realizar a compra :warning:
: Verifique o saldo da sua Wallet com o comando `!fb` `saldo`
"""

LOJA_ITEM_PRICE_CHANGED = """
Ops, parece que o preço do item que você tentou comprar foi alterado :warning:
: Verifique os preços atualizados com o comando `!fb` `loja`
"""

LOJA_ITEM_UNAVAILABLE = """
Ops, parece que o item que você tentou comprar não está mais disponível :warning:
: Verifique os itens disponíveis com o comando `!fb` `loja`
"""

LOJA_WALLET_NOT_FOUND = """
Ops, parece que você não tem uma wallet no FabBank. Você precisa de uma para comprar na loja :warning:
: Para criar uma wallet fale com o Fabs
"""


### FABBANK EXTRATO ###

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
