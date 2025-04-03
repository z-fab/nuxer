# from fabbank.use_cases.consultar_saldo import ConsultarSaldo
from fabbank.command_router import handle_fabbank
from shared.dto.slack_command_input import SlackCommandInput


def handle_command(input_data: SlackCommandInput):
    input_data.set_status("Pensando...")

    match input_data.command:
        case "fabbank" | "fb":
            handle_fabbank(input_data)
        case _:
            input_data.say("Comando não reconhecido.")
