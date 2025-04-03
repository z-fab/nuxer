# fabbank/use_cases/consultar_saldo.py


from shared.dto.slack_command_input import SlackCommandInput


class ConsultarSaldo:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self):
        self.input.say("Saldo")

        return True
        # user = get_users_by_slack_id(self.input.user_id)
        # if not user:
        #     self.input.say("Usuário não encontrado.")
        #     return

        # service = FabBankService(user)
        # try:
        #     balance, wallet_id = service.get_saldo()
        #     text = f"{user.name}, você tem {balance} Fabcoins na sua conta."
        #     self.input.say(text)
        # except Exception:
        #     self.input.say(msg.MSG_ERROR)
