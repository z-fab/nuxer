from datetime import datetime

from config.const import CONST_ERROR
from externals.context import Context
from models.entities.item_loja_entity import ItemLojaEntity
from models.entities.user_entity import UserEntity
from repositories import fabbank_repository as fbr
from repositories.configs_repository import get_config_by_name, save_config_value
from utils import slack_utils as slack_utils

context = Context()


class FabBankService:
    USER: UserEntity = None

    def __init__(self, user: UserEntity = None):
        self.USER = user

    # GETTERS
    def get_saldo(self):
        wallet = fbr.get_wallet_by_user_id(self.USER.id)
        return wallet.balance, wallet.wallet_id

    def get_total_coins(self):
        all_wallets = fbr.get_all_wallets()
        sum_coins = 0
        for wallet in all_wallets:
            sum_coins += wallet.balance
        return sum_coins

    def get_preco_item(self, item: ItemLojaEntity):
        if not item.valor_real:
            return item.valor

        # Obter dados básicos
        total_fabcoins = self.get_total_coins()
        reserva_real = int(get_config_by_name("RESERVA_REAL").value)

        # Definir limite mínimo de segurança (15% da reserva nunca será usada)
        reserva_segura = reserva_real * 0.85

        # Taxa de câmbio base (ajustada pela proporção da reserva já utilizada)
        proporcao_reserva_usada = max(0, min(1, (reserva_real - reserva_segura) / reserva_real))
        taxa_cambio_base = total_fabcoins / reserva_real

        # Fator de escassez: aumenta o preço quando a reserva diminui
        fator_escassez = 1 + (1 - proporcao_reserva_usada) ** 2

        # Variação semanal (5% para mais ou para menos)
        dia_semana = datetime.now().weekday()  # 0-6 (segunda a domingo)
        fator_semanal = 0.95 + (dia_semana / 60)  # Varia de 0.95 a 1.05 ao longo da semana

        # Variação horária (10% para mais ou para menos)
        hora_atual = datetime.now().hour
        # Preços mais altos no meio do dia, mais baixos à noite
        if 11 <= hora_atual < 17:
            # Horário comercial: preços mais altos
            fator_horario = 1.0 + (min(abs(14 - hora_atual), 5) * 0.02)  # Pico às 13h
        else:
            # Fora do horário comercial: preços mais baixos
            fator_horario = 0.9 + (min(hora_atual, 24 - hora_atual) * 0.01)  # Mínimo à meia-noite

        return round(item.valor * taxa_cambio_base * fator_escassez * fator_semanal * fator_horario)

    # SETTERS
    def change_coins(self, user_to: UserEntity, value: int, description: str):
        wallet_from = fbr.get_wallet_by_user_id(0)
        wallet_to = fbr.get_wallet_by_user_id(user_to.id)

        if wallet_to is None:
            raise ValueError(CONST_ERROR.FABBANK_TRANSFER_WALLET_NOT_FOUND)

        if description == "":
            raise ValueError(CONST_ERROR.FABBANK_TRANSFER_PARAMS)

        # Verifica se é para adicionar ou remover moedas
        if value >= 0:
            result = fbr.add_coins(wallet_to, value)
        else:
            result = fbr.remove_coins(wallet_to, abs(value))

        if not result:
            raise ValueError(CONST_ERROR.FABBANK_CHANGE_COINS_FAILED)

        result = fbr.create_transaction(wallet_from, wallet_to, value, description)

        if not result:
            raise ValueError(CONST_ERROR.FABBANK_CHANGE_COINS_FAILED)

        return True

    def transfer_coins(self, user_to: UserEntity, value: int, description: str):
        if user_to is None or self.USER is None:
            raise ValueError(CONST_ERROR.FABBANK_TRANSFER_USER_NOT_FOUND)

        wallet_to = fbr.get_wallet_by_user_id(user_to.id)
        wallet_from = fbr.get_wallet_by_user_id(self.USER.id)

        if wallet_to is None:
            raise ValueError(CONST_ERROR.FABBANK_TRANSFER_WALLET_NOT_FOUND)

        if wallet_from is None:
            raise ValueError(CONST_ERROR.FABBANK_TRANSFER_WALLET_NOT_FOUND)

        if value <= 0:
            raise ValueError(CONST_ERROR.FABBANK_TRANSFER_PARAMS)
        elif value > wallet_from.balance:
            raise ValueError(CONST_ERROR.FABBANK_TRANSFER_INSUFFICIENT_BALANCE)

        if description == "":
            raise ValueError(CONST_ERROR.FABBANK_TRANSFER_PARAMS)

        result = fbr.remove_coins(wallet_from, value)
        if result:
            result = fbr.add_coins(wallet_to, value)

        if result:
            fbr.create_transaction(wallet_from, wallet_to, value, description)
            return True
        else:
            raise RuntimeError(CONST_ERROR.FABBANK_TRANSFER_FAILED)

    def comprar_item(self, item: ItemLojaEntity):
        wallet = fbr.get_wallet_by_user_id(self.USER.id)
        value = self.get_preco_item(item)

        if item is None:
            raise ValueError(CONST_ERROR.FABBANK_LOJA_ITEM_NOT_FOUND)

        # Verificando se o usuário tem saldo suficiente
        if int(wallet.balance) < item.valor:
            raise ValueError(CONST_ERROR.FABBANK_LOJA_INSUFFICIENT_BALANCE)

        # Verificando se o item está disponível
        if item.amount == 0 or not item.enable:
            raise ValueError(CONST_ERROR.FABBANK_LOJA_ITEM_UNAVAILABLE)

        # Realizando a compra
        result = fbr.remove_coins(wallet, value)

        if not result:
            raise RuntimeError(CONST_ERROR.FABBANK_LOJA_FAILED)

        # Atualizando a quantidade do item
        if item.valor_real:
            reserva_real_orm = get_config_by_name("RESERVA_REAL")
            save_config_value(
                reserva_real_orm,
                str(int(reserva_real_orm.value) - item.valor),
            )

        return fbr.create_transaction(
            fbr.get_wallet_by_user_id(0),
            wallet,
            value * (-1),
            "Compra de item na Lojinha do Nuxer: " + item.nome,
        )

    # def get_extrato(self, params: List[str]):
    #     wallet = fbr.get_wallet_by_user_id(self.user.id)[0]
    #     transactions = fbr.get_transactions_by_wallet_to(wallet.wallet_id)

    #     extract = ""
    #     for transaction in transactions[:10]:
    #         wallet_from = fbr.get_wallet_by_id(transaction.wallet_from)
    #         extract += CONST_MESSAGE.TEMPLATE_FABCOIN_EXTRACT_TRANSACTION.format(
    #             user_from=wallet_from.user.nome,
    #             id_wallet_from=wallet_from.wallet_id,
    #             amount=transaction.amount,
    #             description=transaction.description,
    #             timestamp=transaction.timestamp.strftime("%d/%m/%Y %H:%M:%S"),
    #         )

    #     text = CONST_MESSAGE.TEMPLATE_FABCOIN_EXTRACT.format(
    #         apelido=self.user.apelido,
    #         balance=wallet.balance,
    #         id_wallet=wallet.wallet_id,
    #         data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    #         extract=extract,
    #     )

    #     context.slack.send_dm(
    #         user=self.user.slack_id,
    #         text=text,
    #         alt_text="🪙 Seu extrato de Fabcoins",
    #     )
