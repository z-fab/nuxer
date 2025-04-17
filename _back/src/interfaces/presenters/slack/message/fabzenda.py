from datetime import datetime

from domains.fabzenda import messages as MSG
from domains.fabzenda.entities.user_animal import UserAnimalEntity


class FabzendaSlackPresenter:
    def __init__(self, now: datetime | None = None):
        self.now = now or datetime.now()

    def fabzenda_option(self) -> str:
        return MSG.FABZENDA_OPTIONS

    def notificate_animal_dead(self, animal: UserAnimalEntity) -> str:
        return MSG.NOTIFICATION_ANIMAL_DEAD.format(
            apelido=animal.user.apelido,
            emoji=animal.animal_type.emoji,
            name=animal.name,
        )

    def notificate_channel_animal_dead(self, animal: UserAnimalEntity) -> str:
        return MSG.NOTIFICATION_CHANNEL_ANIMAL_DEAD.format(
            slack_id=animal.user.slack_id,
            emoji=animal.animal_type.emoji,
            name=animal.name,
        )

    def notificate_animal_sick(self, animal: UserAnimalEntity) -> str:
        return MSG.NOTIFICATION_ANIMAL_SICK.format(
            apelido=animal.user.apelido,
            emoji=animal.animal_type.emoji,
            name=animal.name,
            feeding_cost=animal.feeding_cost,
            id=animal.animal_id,
        )
