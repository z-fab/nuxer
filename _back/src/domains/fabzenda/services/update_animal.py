from datetime import datetime, timedelta
from math import floor

from loguru import logger

from domains.fabzenda.repositories.user_animal import UserAnimalRepository
from shared.dto.service_response import ServiceResponse
from shared.infrastructure.db_context import DatabaseExternal


class UpdateAnimalService:
    def __init__(self, db_context: DatabaseExternal):
        self.user_animal_repository = UserAnimalRepository(db_context)

    def update_animals_status(self):
        all_users_animals = self.user_animal_repository.get_all_user_animals_alive()

        sick_animals = []
        dead_animals = []

        for user_animal in all_users_animals:
            last_fed = user_animal.last_fed
            hunger_rate = user_animal.hunger_rate

            # Calculando o tempo decorrido excluindo finais de semana
            current_time = datetime.now()
            hours_elapsed = 0

            # Iterando por cada hora desde o último alimentado
            temp_time = last_fed
            while temp_time < current_time:
                # Verificando se é final de semana (5=sábado, 6=domingo)
                if temp_time.weekday() < 5:  # Se não for final de semana
                    hours_elapsed += 1

                temp_time += timedelta(hours=1)

            slots_used = floor(hours_elapsed / hunger_rate)

            # Atualizando os slots de fome
            user_animal.food_slot = 0
            if slots_used <= 4:
                user_animal.food_slot = 4 - slots_used

            # Atualizando a saúde do animal
            old_health = user_animal.health
            user_animal.health = 4
            if slots_used == 4:
                user_animal.health = 3
            elif slots_used == 5:
                user_animal.health = 2
            elif slots_used == 6:
                user_animal.health = 1
                if old_health > 1:
                    sick_animals.append(user_animal)
            elif slots_used >= 7:
                user_animal.health = 0
                if old_health > 0:
                    dead_animals.append(user_animal)

            self.user_animal_repository.update_user_animal(user_animal)

        logger.info("Atualização de status dos animais realizada com sucesso")
        return ServiceResponse(
            success=True,
            data={
                "sick_animals": sick_animals,
                "dead_animals": dead_animals,
            },
        )
