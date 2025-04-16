from collections.abc import Callable
from datetime import datetime
from typing import Any

from _back.src.fabbank.services.fabbank_service import FabBankService
from actions.action import Action
from config.const import CONST_MESSAGE, CONST_SLACK
from externals.context import Context
from loguru import logger
from repositories.fabbank_repository import (
    get_all_enabled_items,
    get_item_by_cod,
)

from models.entities.item_loja_entity import ItemLojaEntity
from models.entities.user_entity import UserEntity

context = Context()


class FabBankAction(Action):
    PARAMS: list = []
    SET_STATUS: Callable[..., Any] = None
    SAY: Callable[..., Any] = None
    OPEN_VIEW: Callable[..., Any] = None
    USER: UserEntity = None

    def __init__(
        self,
        user: UserEntity,
        params: list,
        set_status: Callable[..., Any],
        say: Callable[..., Any],
        open_view: Callable[..., Any],
    ):
        self.PARAMS = params
        self.SET_STATUS = set_status
        self.SAY = say
        self.USER = user
        self.OPEN_VIEW = open_view

    def _opt_saldo(self):
        fbs = FabBankService(self.USER)
        balance, wallet_id = fbs.get_saldo()

        text = CONST_MESSAGE.TEMPLATE_FABBANK_WALLET.format(
            balance=balance,
            apelido=self.USER.apelido,
            id_wallet=wallet_id,
            data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        )

        self.SAY(text)

    # def _opt_pix(self):
    #     if len(self.PARAMS) < 4:
    #         self.SAY(
    #             CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS,
    #             "Houve um erro ao transferir Fabcoins",
    #         )
    #         return False

    #     to = self.PARAMS[1].replace("<@", "").replace(">", "")
    #     user_to = get_users_by_slack_id(to)
    #     value = int(self.PARAMS[2])
    #     description = self.PARAMS[3]

    #     if not user_to or not value or not description:
    #         self.SAY(
    #             CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS,
    #             "Houve um erro ao transferir Fabcoins",
    #         )
    #         return False

    #     fbs = FabBankService(self.USER)

    #     try:
    #         fbs.transfer_coins(user_to, value, description)
    #         wallet_from = get_wallet_by_user_id(self.USER.id)
    #         wallet_to = get_wallet_by_user_id(user_to.id)

    #         text_success = CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_SUCCESS.format(
    #             apelido=self.USER.apelido,
    #             amount=value,
    #             to_name=user_to.nome,
    #             desc=description,
    #             id_wallet=wallet_from.wallet_id,
    #             to_id_wallet=wallet_to.wallet_id,
    #             data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    #         )
    #         self.SAY(text_success, "🪙 Transferência de Fabcoins recebida")

    #         text_receive = CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_RECEIVE.format(
    #             to_apelido=user_to.apelido,
    #             amount=value,
    #             from_name=self.USER.nome,
    #             from_id_wallet=wallet_from.wallet_id,
    #             desc=description,
    #         )
    #         context.slack.send_dm(
    #             user=user_to.slack_id,
    #             text=text_receive,
    #             alt_text="🪙 Transferência de Fabcoins recebida",
    #         )

    #     except Exception as e:
    #         match str(e):
    #             case CONST_ERROR.FABBANK_TRANSFER_USER_NOT_FOUND:
    #                 text_error = CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_ERROR_USER_NOT_FOUND
    #             case CONST_ERROR.FABBANK_TRANSFER_WALLET_NOT_FOUND:
    #                 text_error = CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_ERROR_WALLET_NOT_FOUND
    #             case CONST_ERROR.FABBANK_TRANSFER_INSUFFICIENT_BALANCE:
    #                 text_error = CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_ERROR_INSUFFICIENT_BALANCE
    #             case CONST_ERROR.FABBANK_TRANSFER_PARAMS:
    #                 text_error = CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS
    #             case _:
    #                 raise e

    #         self.SAY(
    #             text_error,
    #             "Houve um erro ao transferir Fabcoins",
    #         )

    #     return True

    # def _opt_change(self):
    #     if self.USER.role > 0:
    #         self.SAY(
    #             CONST_MESSAGE.MESSAGE_COMMAND_ADMIN_ONLY,
    #             "Ops! Você não tem autorização :eyes:",
    #         )
    #         return False

    #     to = self.PARAMS[1].replace("<@", "").replace(">", "")
    #     user_to = get_users_by_slack_id(to)
    #     value = int(self.PARAMS[2])
    #     description = self.PARAMS[3]

    #     if not user_to or not value or not description or value == 0:
    #         self.SAY(
    #             CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS,
    #             "Houve um erro ao adicionar Fabcoins",
    #         )
    #         return False

    #     fbs = FabBankService(self.USER)

    #     try:
    #         fbs.change_coins(user_to, value, description)
    #         wallet_from = get_wallet_by_user_id(0)
    #         wallet_to = get_wallet_by_user_id(user_to.id)

    #         text_success = CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_SUCCESS.format(
    #             apelido="FabBank",
    #             amount=value,
    #             to_name=user_to.nome,
    #             desc=description,
    #             id_wallet=wallet_from.wallet_id,
    #             to_id_wallet=wallet_to.wallet_id,
    #             data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    #         )
    #         self.SAY(text_success, "🪙 Transferência de Fabcoins enviada")
    #         if value > 0:
    #             alt_text = "🪙 Transferência de Fabcoins recebida"
    #             text_receive = CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_RECEIVE.format(
    #                 to_apelido=user_to.apelido,
    #                 amount=value,
    #                 from_name="FabBank",
    #                 from_id_wallet=wallet_from.wallet_id,
    #                 desc=description,
    #             )
    #         else:
    #             alt_text = "🪙 Desconto de Fabcoins recebido"
    #             text_receive = CONST_MESSAGE.TEMPLATE_FABBANK_DISCOUNT_RECEIVE.format(
    #                 to_apelido=user_to.apelido,
    #                 amount=abs(value),
    #                 from_name="FabBank",
    #                 from_id_wallet=wallet_from.wallet_id,
    #                 desc=description,
    #             )

    #         context.slack.send_dm(
    #             user=user_to.slack_id,
    #             text=text_receive,
    #             alt_text=alt_text,
    #         )

    #     except Exception as e:
    #         match str(e):
    #             case CONST_ERROR.FABBANK_TRANSFER_WALLET_NOT_FOUND:
    #                 text_error = CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_ERROR_WALLET_NOT_FOUND
    #             case CONST_ERROR.FABBANK_CHANGE_COINS_FAILED:
    #                 text_error = CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_ERROR_INSUFFICIENT_BALANCE
    #             case CONST_ERROR.FABBANK_TRANSFER_PARAMS:
    #                 text_error = CONST_MESSAGE.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS
    #             case _:
    #                 raise e

    #         self.SAY(text_error)

    #     return True

    def _opt_loja(self):
        fbs = FabBankService(self.USER)
        all_items: list[ItemLojaEntity] = get_all_enabled_items()

        items = ""
        for item in all_items:
            if item.amount > 0 or item.amount == -1:
                preco_item = fbs.get_preco_item(item)

                items += CONST_MESSAGE.TEMPLATE_FABBANK_LOJA_ITEM.format(
                    id=item.cod,
                    item=item.nome,
                    price=preco_item,
                    description=item.descricao,
                    amount=f": Quantidade Disponível: {item.amount}" if item.amount > 0 else "",
                )

        fbs = FabBankService(self.USER)
        balance, _ = fbs.get_saldo()
        text = CONST_MESSAGE.TEMPLATE_FABBANK_LOJA.format(
            balance=balance,
            items=items,
        )

        self.SAY(text, "Vendinha do Uxer 🛍️")

    def _opt_comprar(self):
        item = get_item_by_cod(self.PARAMS[1])

        if not item:
            self.SAY(
                CONST_MESSAGE.TEMPLATE_FABBANK_LOJA_ITEM_NAO_COMPRADO,
                "Não foi possível comprar o item",
            )
            return False

        try:
            fbs = FabBankService(self.USER)
            fbs.comprar_item(item)

            text = CONST_MESSAGE.TEMPLATE_FABBANK_LOJA_ITEM_COMPRADO.format(
                apelido=self.USER.apelido, item=item.nome, price=item.valor
            )

            self.SAY(text, "Item comprado com sucesso")

            text_admin = CONST_MESSAGE.TEMPLATE_FABBANK_LOJA_ITEM_COMPRADO_ADMIN.format(
                user_from=self.USER.nome,
                item=item.nome,
                price=self.PARAMS[2],
                data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )

            context.slack.send_dm(
                user=CONST_SLACK.ID_USER_ADMIN, text=text_admin, alt_text="Um item foi comprado na lojinha do Nuxer"
            )

        except Exception as e:
            logger.warning(f"Erro ao comprar item: {e}")

            self.SAY(
                CONST_MESSAGE.TEMPLATE_FABBANK_LOJA_ITEM_NAO_COMPRADO.format(
                    apelido=self.USER.apelido, item=item.nome, price=self.PARAMS[2]
                ),
                "Não foi possível comprar o item",
            )
        return True

    def run(self):
        self.SET_STATUS("em contato com FabBank...", False)
        command = self.PARAMS[0]
        match command:
            case "saldo":
                return self._opt_saldo()
            case "pix":
                return self._opt_pix()
            case "change":
                return self._opt_change()
            case "loja":
                return self._opt_loja()
            case "btn_comprar":
                return self._opt_comprar()
            case _:
                self.SAY(CONST_MESSAGE.MESSAGE_COMMAND_FB_HELP, "Comando não encontrado")
                return False

        return True

    #  def __init__(self, payload: dict):
    #     self.payload = payload

    # def __message_help(self):
    #     context.slack.send_dm(
    #         user=self.payload.get("mse").user[0].slack_id,
    #         text=CONST_MESSAGE.MESSAGE_COMMAND_FC_HELP,
    #     )

    # def __saldo(self, fabcoin_s):
    #     if self.payload.get("mse").user[0].slack_id == CONST_SLACK.ID_USER_ADMIN:
    #         fabcoin_s.get_saldo(admin=True)
    #     else:
    #         fabcoin_s.get_saldo()

    # def __remover(self, fabcoin_s, params):
    #     if fabcoin_s.user.slack_id == CONST_SLACK.ID_USER_ADMIN:
    #         print(params)
    #     else:
    #         context.slack.send_dm(
    #             user=self.payload.get("mse").user[0].slack_id,
    #             text=CONST_MESSAGE.MESSAGE_COMMAND_ADMIN_ONLY,
    #         )

    # def __transferir(self, fabcoin_s, params, admin=False):
    #     if admin:
    #         if fabcoin_s.user.slack_id == CONST_SLACK.ID_USER_ADMIN:
    #             fabcoin_s.transferir(params, admin)
    #         else:
    #             context.slack.send_dm(
    #                 user=self.payload.get("mse").user[0].slack_id,
    #                 text=CONST_MESSAGE.MESSAGE_COMMAND_ADMIN_ONLY,
    #             )
    #     else:
    #         fabcoin_s.transferir(params)

    # def __extrato(self, fabcoin_s, params):
    #     fabcoin_s.get_extrato(params)

    # def __loja(self, fabcoin_s, params):
    #     if len(params) == 1:
    #         fabcoin_s.get_itens_loja()

    # def __comprar_item(self, fabcoin_s):
    #     result = fabcoin_s.comprar_item(self.payload["id"], self.payload["preco"])
    #     item = fabcoin_s.get_item_by_id(self.payload["id"])

    #     if result:
    #         text = CONST_MESSAGE.TEMPLATE_FABBANK_LOJA_ITEM_COMPRADO.format(
    #             apelido=self.payload.get("ase").user[0].apelido,
    #             item=item.get("nome"),
    #             price=self.payload["preco"],
    #         )

    #         context.slack.send_dm(
    #             user=self.payload.get("ase").user[0].slack_id, text=text
    #         )

    #         text = CONST_MESSAGE.TEMPLATE_FABBANK_LOJA_ITEM_COMPRADO_ADMIN.format(
    #             user_from=self.payload.get("ase").user[0].nome,
    #             item=item.get("nome"),
    #             price=self.payload["preco"],
    #             data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    #         )

    #         context.slack.send_dm(user=CONST_SLACK.ID_USER_ADMIN, text=text)

    #         return True

    #     else:
    #         text = CONST_MESSAGE.TEMPLATE_FABBANK_LOJA_ITEM_NAO_COMPRADO.format(
    #             apelido=self.payload.get("ase").user[0].apelido,
    #             item=item.get("nome"),
    #             price=self.payload["preco"],
    #         )

    #         context.slack.send_dm(
    #             user=self.payload.get("ase").user[0].slack_id,
    #             text=text,
    #         )

    #         return True

    # def execute(self):
    #     # Commands via message
    #     if "mse" in self.payload:
    #         params = self.payload.get("mse").params
    #         user = self.payload.get("mse").user

    #         if isinstance(user, list) and len(user) > 0:
    #             user = user[0]

    #         if len(params) == 0:
    #             self.__message_help()
    #             return False

    #         fabcoin_s = FabcoinService(user)

    #         match params[0]:
    #             case "saldo":
    #                 self.__saldo(fabcoin_s)
    #             case "pix":
    #                 self.__transferir(fabcoin_s, params)
    #             case "add":
    #                 self.__transferir(fabcoin_s, params, admin=True)
    #             case "remove":
    #                 self.__remover(fabcoin_s, params)
    #             case "extrato":
    #                 self.__extrato(fabcoin_s, params)
    #             case "loja":
    #                 self.__loja(fabcoin_s, params)
    #             case "help":
    #                 self.__message_help()
    #             case _:
    #                 self.__message_help()
    #                 return False

    #         return True

    #     # Commands via actions
    #     elif "ase" in self.payload:
    #         fabcoin_s = FabcoinService(self.payload.get("ase").user[0])
    #         match self.payload.get("action"):
    #             case "comprar_item":
    #                 return self.__comprar_item(fabcoin_s)
    #             case _:
    #                 return False

    #     return False
