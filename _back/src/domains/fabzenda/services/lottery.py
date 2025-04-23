import random
from collections import defaultdict

from domains.config.repositories.config import ConfigRepository
from domains.fabbank.services.transaction import TransactionService
from domains.fabzenda.entities.animal_type import AnimalTypeEntity
from domains.fabzenda.entities.user_animal import UserAnimalEntity
from domains.fabzenda.repositories.animal_type import AnimalTypeRepository
from domains.fabzenda.repositories.user_animal import UserAnimalRepository
from shared.dto.service_response import ServiceResponse
from shared.infrastructure.db_context import DatabaseExternal


class LotteryService:
    def __init__(self, db_context: DatabaseExternal):
        self.animal_type_repository = AnimalTypeRepository(db_context)
        self.user_animal_repository = UserAnimalRepository(db_context)
        self.transaction_service = TransactionService(db_context)
        self.config_repository = ConfigRepository(db_context)

    def _can_animal_participate(self, animal: UserAnimalEntity) -> bool:
        return animal.is_alive and animal.reward > 0 and animal.health > 0

    def _pay_winners(self, dict_winners: dict) -> bool:
        for user_id, info in dict_winners.items():
            total_reward = info["total_reward"]

            self.transaction_service.change_coins(
                to_id=user_id,
                value=total_reward,
                description="[Fabzenda] Premio - Jogo dos Fabichinhos",
            )

    def run_lottery(self) -> ServiceResponse:
        all_animals = self.animal_type_repository.get_all_available()
        n_lottery = self.config_repository.get_config_by_name("N_LOTTERY")
        winning_types: list[AnimalTypeEntity] = random.sample(all_animals, int(n_lottery.value))

        animal_winners_by_user = defaultdict(list)
        for winning_type in winning_types:
            user_animals: list[UserAnimalEntity] = self.user_animal_repository.get_user_animals_alive_by_type_id(
                winning_type.type_id
            )

            for animal in user_animals:
                if self._can_animal_participate(animal):
                    animal_winners_by_user[animal.user_id].append(animal)

        # Calculando premio
        dict_winners = {}
        for user_id, user_animals in animal_winners_by_user.items():
            distinct_animals = [animal.animal_type.type_id for animal in user_animals]
            distinct_animals = set(distinct_animals)

            total_reward = sum([animal.reward for animal in user_animals])
            if len(distinct_animals) == 3:
                total_reward = int(total_reward * 1.15)
            elif len(distinct_animals) == 4:
                total_reward = int(total_reward * 1.30)
            elif len(distinct_animals) == 5:
                total_reward = int(total_reward * 2)

            dict_winners[user_id] = {
                "animals": user_animals,
                "n_distinct_animals": len(distinct_animals),
                "total_reward": total_reward,
            }

        # Pagando os ganhadores
        if len(dict_winners) > 0:
            self._pay_winners(dict_winners)

        return ServiceResponse(
            success=True,
            data={
                "winning_types": winning_types,
                "winners": dict_winners,
            },
        )
