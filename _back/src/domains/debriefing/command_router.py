from domains.debriefing.use_cases.validar_debriefing import ValidarDebriefing
from interfaces.presenters.hints import DebriefingHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse


def handle_debriefing(input_data: SlackCommandInput, set_status: callable) -> UseCaseResponse:
    set_status("Consultando Debriefings...")

    option = ""
    if len(input_data.args) > 0:
        option = input_data.args[0]

    match option:
        case "ver_debriefing":
            pass
        case "validar_debriefing":
            return ValidarDebriefing(input_data.args[1], input_data.user_id)()
        case _:
            return UseCaseResponse(
                success=True,
                notification=[
                    {"presenter_hint": DebriefingHints.DEBRIEFING_OPTIONS},
                ],
            )
