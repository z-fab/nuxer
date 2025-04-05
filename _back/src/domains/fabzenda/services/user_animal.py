from datetime import datetime

from domains.fabzenda import messages as MSG
from domains.fabzenda.repositories.user_animal import UserAnimalRepository
from domains.user.repositories.user import UserRepository
from shared.dto.use_case_response import UseCaseResponse


class UserAnimalService:
    def __init__(self, user_animal_repo: UserAnimalRepository, user_repo: UserRepository):
        self.user_repository: UserRepository = user_repo
        self.user_animal_repository: UserAnimalRepository = user_animal_repo

    def show_fabzenda(self, user_id: str) -> UseCaseResponse:
        title_view = "Sua Fabzenda 🏕️"
        user = self.user_repository.get_user_by_id(user_id)

        # Obter o animal do usuário
        user_animals = self.user_animal_repository.get_user_animals_alive_by_user_id(user_id)

        # Verificando se há animais na fabzenda
        if len(user_animals) <= 0:
            message = MSG.TEMPLATE_FABZENDA_FAZENDA_VAZIA.format(apelido=user.apelido)
            return UseCaseResponse(message=message, data={"animals": [], "title_view": title_view}, success=False)

        slots_fabzenda = [f"{animal.animal_type.emoji}" for animal in user_animals]

        animals_text = ""
        for animal in user_animals:
            # Verificando se o animal está morto
            if animal.health == 0:
                animals_text += MSG.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_MORTO.format(
                    emoji=animal.animal_type.emoji,
                    burial_cost=animal.burial_cost,
                    type=animal.animal_type.name,
                    name=animal.name,
                    health=animal.health_str,
                    id=animal.animal_id,
                )
                continue

            # Verificando se o animal foi Abduzido
            if (animal.expiry_date < datetime.now()) or (animal.health == -1):
                animals_text += MSG.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_EXPIRADO.format(
                    emoji=animal.animal_type.emoji,
                    expire_value=animal.expire_value,
                    type=animal.animal_type.name,
                    name=animal.name,
                    id=animal.animal_id,
                )
                continue

            food_slot_full = " `🍔` " * animal.food_slot
            food_slot_empty = " `‧` " * (4 - animal.food_slot)
            hunger = f"{food_slot_full}{food_slot_empty}"

            age = (datetime.now() - animal.purchase_date).days

            map_health_description = {
                4: MSG.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_4,
                3: MSG.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_3,
                2: MSG.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_2,
                1: MSG.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_1,
            }
            health_description = map_health_description.get(
                animal.health, MSG.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_4
            )

            animals_text += MSG.TEMPLATE_FABZENDA_FAZENDA_ANIMAL.format(
                emoji=animal.animal_type.emoji,
                type=animal.animal_type.name,
                name=animal.name,
                reward=animal.reward,
                expire_value=animal.expire_value,
                modifier=f"{animal.modifier.name} {animal.modifier.emoji}" if animal.modifier else "Normal 🌱",
                modifier_description=animal.modifier.resume_modifier
                if animal.modifier
                else "Seu fabichinho é normal (mas continua especial)",
                health=animal.health_str,
                health_description=health_description,
                hunger=hunger,
                hunger_rate=animal.hunger_rate,
                age=f"{age} dias" if age > 1 else f"{age} dia" if age == 1 else "Recém-nascido",
                lifespan=animal.lifespan,
                feeding_cost=animal.feeding_cost,
                id=animal.animal_id,
                primary="P" if (animal.food_slot == 0 or animal.health < 4) else "",
            )

        message = MSG.TEMPLATE_FABZENDA_FAZENDA.format(
            apelido=user.apelido, slots=" ".join(slots_fabzenda), animals=animals_text
        )

        return UseCaseResponse(message=message, data={"animals": user_animals, "title_view": title_view}, success=True)
