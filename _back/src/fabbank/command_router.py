from fabbank.use_cases.consultar_saldo import ConsultarSaldo
from shared.dto.slack_command_input import SlackCommandInput


def handle_fabbank(input_data: SlackCommandInput) -> bool:
    input_data.set_status("Falando com FabBank...")

    match input_data.args[0]:
        case "saldo":
            return ConsultarSaldo(input_data)()
        case _:
            input_data.say("Opção não reconhecida para fabbank.")
            return False
