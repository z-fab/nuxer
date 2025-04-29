from domains.debriefing.services.debriefing import DebriefingService
from interfaces.presenters.hints import DebriefingHints
from shared.dto.use_case_response import UseCaseResponse


class NotificarDebriefing:
    def __init__(self, id_page: str):
        self.id_page = id_page.replace("-", "")

    def __call__(self) -> UseCaseResponse:
        debriefing_service = DebriefingService()
        service_response = debriefing_service.notificar_debriefing(self.id_page)

        if not service_response.success:
            return UseCaseResponse(
                success=False,
                error=service_response.error,
                notification=[],
            )

        return UseCaseResponse(
            success=True,
            data=service_response.data,
            notification=[
                {
                    "presenter_hint": DebriefingHints.DEBRIEFING_NOTIFICATE_SOLICITANTE,
                    "user": service_response.data["solicitante"],
                },
            ],
        )
