from domains.debriefing.repositories.debriefing import DebriefingRepository
from domains.debriefing.types.status import DebriefingStatus
from domains.fabbank.services.transaction import TransactionService
from interfaces.presenters.hints import DebriefingHints
from shared.dto.service_response import ServiceResponse
from shared.infrastructure.db_context import DatabaseExternal


class DebriefingService:
    def __init__(self, db_context: DatabaseExternal | None = None):
        self.debriefing_repository = DebriefingRepository()
        self.transaction_service = TransactionService(db_context)

    def notificar_debriefing(self, id_page: str) -> ServiceResponse:
        debriefing_entity = self.debriefing_repository.get_debriefing_by_page_id(id_page.replace("-", ""))

        # Verifica se o debriefing existe
        if not debriefing_entity:
            return ServiceResponse(success=False, error=DebriefingHints.DEBRIEFING_NOT_FOUND)

        # Verifica se há solicitantes associados
        if (debriefing_entity.solicitante is None) or len(debriefing_entity.solicitante) == 0:
            return ServiceResponse(
                success=False,
                data={"criado_por": debriefing_entity.criado_por},
                error=DebriefingHints.DEBRIEFING_SOLICITANTE_NOT_FOUND,
            )

        # Verifica se o debriefing está concluído
        if (
            debriefing_entity.status == DebriefingStatus.NAO_CONCLUIDO
            or debriefing_entity.status == DebriefingStatus.SEM_ESTIMATIVA
        ):
            return ServiceResponse(
                success=False,
                data={"criado_por": debriefing_entity.criado_por},
                error=DebriefingHints.DEBRIEFING_NOT_COMPLETED,
            )

        # Atualiza a data de envio do debriefing
        if not self.debriefing_repository.update_ultimo_envio(debriefing_entity.id):
            return ServiceResponse(success=False, error=DebriefingHints.DEBRIEFING_NOTIFICATE_ERROR)

        data = {
            "titulo": debriefing_entity.titulo,
            "cod": debriefing_entity.cod,
            "id": debriefing_entity.id,
            "url": debriefing_entity.url,
            "criado_por": debriefing_entity.criado_por,
            "solicitante": debriefing_entity.solicitante,
        }

        # Se o debriefing não tinha sido enviado, adiciona fabcoins
        if debriefing_entity.enviado_em is None:
            transfer_response = self.transaction_service.change_coins(
                to_id=debriefing_entity.criado_por.id,
                value=5,
                description=f"[Debriefing] Envio do Debriefing {debriefing_entity.titulo}",
            )

            if transfer_response.success:
                data = data | transfer_response.data

        return ServiceResponse(
            success=True,
            data=data,
        )
