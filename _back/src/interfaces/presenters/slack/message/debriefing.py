from datetime import datetime

from domains.debriefing import message as MSG
from domains.user.entities.user import UserEntity


class DebriefingSlackPresenter:
    def __init__(self, now: datetime | None = None):
        self.now = now or datetime.now()

    def debriefing_option(self) -> str:
        return "options"

    def debriefing_notificate_solicitante(
        self, titulo: str, id: str, criado_por: UserEntity, solicitante: UserEntity, **kwarg
    ) -> str:
        return MSG.DEBRIEFING_NOTIFICATE_SOLICITANTE.format(
            solicitante=solicitante.apelido, criado_por=criado_por.nome, titulo=titulo, id=id
        )

    def debriefing_not_completed(self, **kwarg) -> str:
        return MSG.DEBRIEFING_NOT_COMPLETED
