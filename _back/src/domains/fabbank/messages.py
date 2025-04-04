TEMPLATE_FABBANK_WALLET_NOT_FOUND = """
Ops, parece que você não tem uma wallet no FabBank :warning:
: Para criar uma fale com o Fabs
"""

### FABBANK WALLET ###

TEMPLATE_FABBANK_WALLET = """
# Extrato do FabBank :moneybag:
{apelido}, aqui está o saldo da sua Wallet:
> *Saldo atual*: `F₵ {balance}`
: Wallet ID: {id_wallet} - Valores atualizados em {data}
"""


TEMPLATE_FABBANK_WALLET_ADMIN = """
# Saldos no Fabbank
Aqui estão os saldos no Fabbank
> *Saldo Total*: `F₵ {balance_total}`
--
{balances}
"""

### FABBANK TRANSFERÊNCIA ###

TEMPLATE_FABBANK_TRANSFER_SUCCESS = """
# Transferência Realizada com Sucesso :money_with_wings:
{apelido}, você realizou uma transferência com o sucesso.
> *Você transferiu* `F₵ {amount}` para `{to_name} (Wallet ID: {to_id_wallet})`
*Motivo informado:* _{desc}_
: Wallet ID: {id_wallet} - transação realizada em {data}
"""

TEMPLATE_FABBANK_TRANSFER_RECEIVE = """
# Recebimento de Transferência :moneybag:
{to_apelido}, você recebeu uma transferência em sua Wallet.
> *Você recebeu* `F₵ {amount}` de `{from_name} (Wallet ID: {from_id_wallet})`
*Motivo informado:* _{desc}_
"""

TEMPLATE_FABBANK_DISCOUNT_RECEIVE = """
# Desconto Aplicado :money_with_wings:
{to_apelido}, você recebeu um desconto em sua Wallet.
> *Você foi descontado* em `F₵ {amount}` pelo `{from_name} (Wallet ID: {from_id_wallet})`
*Motivo informado:* _{desc}_
"""

TEMPLATE_FABBANK_TRANSFER_ERROR = """
Ops, ocorreu um erro ao realizar a transferência :warning:
: Tente novamente e avise o Fabs
"""

TEMPLATE_FABBANK_TRANSFER_ERROR_USER_NOT_FOUND = """
Ops, parece que o usuário que você escolheu para receber a transferência não tem uma wallet no FabBank :warning:
: Verifique o usuário que você escolheu para receber a transferência e tente novamente
"""

TEMPLATE_FABBANK_TRANSFER_ERROR_WALLET_NOT_FOUND = """
Ops, parece que você (ou a pessoa para quem você quer transferir) não tem uma wallet no FabBank :warning:
: Para criar fale com o Fabs
"""

TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS = """
Ops, parece que você não preencheu corretamente os parâmetros para realizar a transferência :warning:
: Para realizar a transferência, utilize o comando `!fb` `pix` `[@usuario]` `[valor]` `"[descrição]"`
"""

TEMPLATE_FABBANK_TRANSFER_ERROR_INSUFFICIENT_BALANCE = """
Ops, parece que você não tem saldo suficiente para realizar a transferência ou o valor informado é inválido :warning:
: Verifique o saldo da sua Wallet com o comando `!fb` `saldo`
"""

TEMPLATE_FABBANK_TRANSFER_ERROR_PERMISSION = """
Ops, você não tem permissão para realizar essa transferência :warning:
: Como você descobriu esse comando? :eyes:
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


#### FABBANK LOJA ####

TEMPLATE_FABBANK_LOJA = """
# Vendinha do Uxer 🛍️
A melhor, maior e única loja do mundo que aceita Fabcoins! Preços atualizados a todo momento.
> Seu saldo: `F₵ {balance}`
--
{items}
"""

TEMPLATE_FABBANK_LOJA_ITEM = """
[ cod: *{id}* ] {item} `F₵ {price}`
: {description}
{amount}
<🛒 Comprar(fb)[opt=btn_comprar,id={id},preco={price}]>
--
"""

TEMPLATE_FABBANK_LOJA_ITEM_COMPRADO = """
# Item Comprado 🛒
{apelido}, você comprou um item da loja com sucesso!
> {item} por `F₵ {price}`
: Já notifiquei o fabs e em breve o item será enviado.
"""

TEMPLATE_FABBANK_LOJA_ITEM_NAO_COMPRADO = """
# Ops, item não comprado 🛒
{apelido}, não foi possível realizar a compra do seu item. Verifique seu saldo ou se o preço do item não foi alterado
> {item} por `F₵ {price}`
: Para verificar seu saldo, utilize o comando `!fb` `saldo` e para verificar os itens com preço atualizado, utilize o comando `!fb` `loja`
"""

TEMPLATE_FABBANK_LOJA_ITEM_COMPRADO_ADMIN = """
--
# Item Comprado 🛍️
{user_from} comprou um item da loja.
> {item} por `F₵ {price}` em {data}
--
"""
