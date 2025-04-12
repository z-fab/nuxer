from domains.fabbank.use_cases.alterar_saldo import AlterarSaldo
from domains.fabbank.use_cases.comprar_item import ComprarItem
from domains.fabbank.use_cases.consultar_saldo import ConsultarSaldo
from domains.fabbank.use_cases.transferir import Transferir
from domains.fabbank.use_cases.ver_loja import VerLoja
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse


def handle_fabbank(input_data: SlackCommandInput, set_status: callable) -> UseCaseResponse:
    set_status("Falando com FabBank...")

    option = ""
    if len(input_data.args) > 0:
        option = input_data.args[0]

    match option:
        case "saldo":
            return ConsultarSaldo(input_data)()
        case "transferir" | "pix":
            return Transferir(input_data)()
        case "change" | "alterar":
            return AlterarSaldo(input_data)()
        case "loja" | "store" | "shop":
            return VerLoja(input_data)()
        case "comprar":
            return ComprarItem(input_data)()
        case _:
            return UseCaseResponse(
                message="Não consegui entender qual comando do FabBank você quer usar :confused:", success=False
            )
