from datetime import datetime

from domains.debriefing import message as MSG
from domains.debriefing.entities.debriefing import DebriefingEntity
from domains.user.entities.user import UserEntity


class DebriefingSlackPresenter:
    def __init__(self, now: datetime | None = None):
        self.now = now or datetime.now()

    def debriefing_validation_success(self, debriefing: DebriefingEntity, **kwargs) -> dict[str, str]:
        return "Debriefing Validado ✅", MSG.DEBRIEFING_VALIDATION_SUCCESS.format(
            cod=debriefing.cod, titulo=debriefing.titulo
        )

    def debriefing_validation_success_channel(
        self, debriefing: DebriefingEntity, validado_por: UserEntity, **kwargs
    ) -> dict[str, str]:
        return MSG.DEBRIEFING_VALIDATION_SUCCESS_CHANNEL.format(
            cod=debriefing.cod,
            titulo=debriefing.titulo,
            validado_por=validado_por.slack_id,
        )
