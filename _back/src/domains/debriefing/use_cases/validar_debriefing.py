from loguru import logger

from domains.debriefing.services.debriefing import DebriefingService
from domains.user.repositories.user import UserRepository
from interfaces.presenters.hints import DebriefingHints
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.db_context import db


class ValidarDebriefing:
    def __init__(self, id_page: str, user_slack_id: str):
        self.user_slack_id = user_slack_id
        self.id_page = id_page.replace("-", "")

    def __call__(self) -> UseCaseResponse:
        user_repository = UserRepository(db)
        user_entity = user_repository.get_user_by_slack_id(self.user_slack_id)

        debriefing_service = DebriefingService(db)
        service_response = debriefing_service.validar_debriefing(self.id_page, user_entity)

        if not service_response.success:
            logger.error(f"[Validar Debriefing] Erro ao validar: {service_response.error}")
            return UseCaseResponse(
                success=False,
                notification=[
                    {"presenter_hint": DebriefingHints.DEBRIEFING_VALIDATION_ERROR},
                ],
            )

        logger.info(f"[Validar Debriefing] Validado com sucesso: {service_response.data['debriefing']}")
        return UseCaseResponse(
            success=True,
            data=service_response.data,
            notification=[
                {
                    "presenter_hint": DebriefingHints.DEBRIEFING_VALIDATION_SUCCESS,
                    "user": service_response.data["validado_por"],
                },
                {
                    "presenter_hint": DebriefingHints.DEBRIEFING_VALIDATION_SUCCESS_CHANNEL,
                    "channel": "gazeta_uxer",
                },
            ],
        )
