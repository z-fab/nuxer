### FABBANK TRANSFERÊNCIA ###


### FABBANK LOJA ###


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
