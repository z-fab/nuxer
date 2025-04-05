from loguru import logger

from domains.fabbank.command_router import handle_fabbank
from domains.fabzenda.command_router import handle_fabzenda
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse


def handle_command(input_data: SlackCommandInput, set_status: callable) -> UseCaseResponse:
    set_status("Pensando...")
    match input_data.command:
        case "fabbank" | "fb":
            return handle_fabbank(input_data, set_status)
        case "fabzenda" | "fz":
            return handle_fabzenda(input_data, set_status)
        case _:
            logger.debug(f"Comando não reconhecido: {input_data.command}")
            return UseCaseResponse(
                message="Desculpe, não entendi qual comando você quer usar :confused:",
                success=False,
            )
