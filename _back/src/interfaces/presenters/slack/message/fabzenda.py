from datetime import datetime

from domains.fabzenda import messages as MSG
from domains.fabzenda.entities.animal_type import AnimalTypeEntity
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

    def notificate_channel_lottery(self, winning_types: list[AnimalTypeEntity], winners: dict, **kwargs) -> str:
        lottery_result = " ‧ ".join([animal.emoji for animal in winning_types])
        if len(winners) == 0:
            return MSG.NOTIFICATION_CHANNEL_LOTERY_NONE.format(
                result=lottery_result,
            )

        total_reward = sum([info["total_reward"] for info in winners.values()])

        ganhadores = ""
        for _, info in winners.items():
            ganhadores += f"> {info['animals'][0].user.nome} ganhou `F₵ {info['total_reward']}` com {' ‧ '.join([animal.animal_type.emoji for animal in info['animals']])}\n"

        n_ganhadores = f"{len(winners)} ganhador" if len(winners) == 1 else f"{len(winners)} ganhadores"

        return MSG.NOTIFICATION_CHANNEL_LOTERY.format(
            result=lottery_result, n_ganhadores=n_ganhadores, total_reward=total_reward, ganhadores=ganhadores
        )

    def notificate_lottery(self, info_winners: dict, **kwargs) -> str:
        animals = " ‧ ".join([animal.animal_type.emoji for animal in info_winners["animals"]])
        reward = info_winners["total_reward"]
        apelido = info_winners["animals"][0].user.apelido

        if info_winners["n_distinct_animals"] == 2:
            bonus = "Sorte está do seu lado! Você conquistou um bônus de 25% por reunir 2 fabichinhos diferentes no sorteio!"
        elif info_winners["n_distinct_animals"] == 3:
            bonus = "Bônus épico! Você recebeu 2x o prêmio por ter conseguido 3 fabichinhos únicos no sorteio!"
        else:
            bonus = ""

        return MSG.NOTIFICATION_LOTERY.format(apelido=apelido, reward=reward, result=animals, bonus=bonus)
