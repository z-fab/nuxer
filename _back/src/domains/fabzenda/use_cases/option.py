from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse


class OptionFabzenda:
    def __init__(self, ucr: UseCaseRequest):
        self.code = ucr.code

    def __call__(self) -> UseCaseResponse:
        return UseCaseResponse(code=self.code, success=True)
