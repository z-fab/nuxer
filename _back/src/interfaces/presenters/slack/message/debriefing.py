from datetime import datetime

from domains.debriefing import message as MSG
from domains.user.entities.user import UserEntity


class DebriefingSlackPresenter:
    def __init__(self, now: datetime | None = None):
        self.now = now or datetime.now()

    def debriefing_option(self) -> str:
        return "options"

    def debriefing_notificate_solicitante(
        self,
        user: UserEntity,
        titulo: str,
        id: str,
        criado_por: UserEntity,
        solicitante: UserEntity,
        url: str,
        cod: str,
        **kwarg,
    ) -> str:
        return MSG.DEBRIEFING_NOTIFICATE_SOLICITANTE.format(
            solicitante=user.apelido, criado_por=criado_por.slack_id, titulo=titulo, id=id, url=url, cod=cod
        )

    def debriefing_notificate_channel(
        self,
        user: UserEntity,
        titulo: str,
        id: str,
        criado_por: UserEntity,
        solicitante: UserEntity,
        url: str,
        cod: str,
        **kwarg,
    ) -> str:
        solicitantes = ">, <@".join([s.slack_id for s in solicitante])
        solicitantes = f"<@{solicitantes}>"

        return MSG.DEBRIEFING_NOTIFICATE_CHANNEL.format(
            solicitantes=solicitantes, criado_por=criado_por.slack_id, titulo=titulo, id=id, url=url, cod=cod
        )

    def debriefing_not_completed(self, **kwarg) -> str:
        return MSG.DEBRIEFING_NOT_COMPLETED

    def debriefing_solicitante_not_found(self, **kwarg) -> str:
        return MSG.DEBRIEFING_SOLICITANTE_NOT_FOUND

    def debriefing_options(self) -> str:
        return MSG.DEBRIEFING_OPTIONS
