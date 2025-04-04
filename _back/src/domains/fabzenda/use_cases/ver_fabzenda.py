from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse


class VerFabzenda:
    def __init__(self, input_data: SlackCommandInput):
        self.input = input_data

    def __call__(self) -> UseCaseResponse:
        return UseCaseResponse(success=True, message="Fabzenda")
