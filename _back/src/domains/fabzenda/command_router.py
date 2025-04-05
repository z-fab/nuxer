from domains.fabzenda import messages as MSG
from domains.fabzenda.use_cases.ver_fabzenda import VerFabzenda
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse


def handle_fabzenda(input_data: SlackCommandInput, set_status: callable) -> UseCaseResponse:
    set_status("Indo para o interior...")

    option = ""
    if len(input_data.args) > 0:
        option = input_data.args[0]

    match option:
        case "ver":
            return VerFabzenda(input_data)()
        case _:
            return UseCaseResponse(message=MSG.TEMPLATE_FABZENDA_OPTIONS, success=True)
