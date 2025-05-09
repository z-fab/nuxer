from loguru import logger

from domains.debriefing.services.debriefing import DebriefingService
from interfaces.presenters.hints import DebriefingHints, FabbankHints
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class NotificarDebriefing:
    def __init__(self, id_page: str):
        self.id_page = id_page.replace("-", "")

    def __call__(self) -> UseCaseResponse:
        debriefing_service = DebriefingService(db)
        service_response = debriefing_service.notificar_debriefing(self.id_page)

        if not service_response.success:
            logger.error(f"[Notificar Debriefing] Erro ao notificar: {service_response.error}")
            if service_response.error == DebriefingHints.DEBRIEFING_NOT_COMPLETED:
                return UseCaseResponse(
                    success=False,
                    error=DebriefingHints.DEBRIEFING_NOT_COMPLETED,
                    notification=[
                        {
                            "presenter_hint": DebriefingHints.DEBRIEFING_NOT_COMPLETED,
                            "user": service_response.data["criado_por"],
                        }
                    ],
                )
            return UseCaseResponse(
                success=False,
                error=service_response.error,
                notification=[],
            )

        notification = [
            {
                "presenter_hint": DebriefingHints.DEBRIEFING_NOTIFICATE_SOLICITANTE,
                "user": service_response.data["solicitante"],
            }
        ]

        if "wallet_to" in service_response.data:
            logger.info(
                f"[Notificar Debriefing] Transferência de fabcoins realizada: {service_response.data['wallet_to']}"
            )
            notification.append(
                {
                    "presenter_hint": FabbankHints.TRANSFER_SUCCESS_NOTIFICATION,
                    "user": service_response.data["criado_por"],
                }
            )

        logger.info(f"[Notificar Debriefing] Notificado: {service_response.data['titulo']}")
        return UseCaseResponse(success=True, data=service_response.data, notification=notification)
