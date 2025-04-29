from domains.debriefing.repositories.debriefing import DebriefingRepository
from interfaces.presenters.hints import DebriefingHints
from shared.dto.service_response import ServiceResponse
from shared.infrastructure.db_context import DatabaseExternal


class DebriefingService:
    def __init__(self, db_context: DatabaseExternal | None = None):
        self.debriefing_repository = DebriefingRepository()

    def notificar_debriefing(self, id_page: str) -> ServiceResponse:
        debriefing_entity = self.debriefing_repository.get_debriefing_by_page_id(id_page.replace("-", ""))

        if not debriefing_entity:
            return ServiceResponse(success=False, error=DebriefingHints.DEBRIEFING_NOT_FOUND)

        return ServiceResponse(
            success=True,
            data={
                "titulo": debriefing_entity.titulo,
                "id": debriefing_entity.id,
                "criado_por": debriefing_entity.criado_por,
                "solicitante": debriefing_entity.solicitante,
            },
        )
