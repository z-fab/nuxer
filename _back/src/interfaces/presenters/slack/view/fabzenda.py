from datetime import datetime

from domains.fabzenda import messages as MSG
from domains.fabzenda.entities.animal_modifier import AnimalModifierEntity
from domains.fabzenda.entities.animal_type import AnimalTypeEntity
from domains.fabzenda.entities.user_animal import UserAnimalEntity
from domains.user.entities.user import UserEntity


class FabzendaSlackPresenter:
    def __init__(self, now: datetime | None = None):
        self.now = now or datetime.now()

    def wallet_not_found(self, **kwargs) -> str:
        return "Canto Bão 🌾", MSG.TEMPLATE_FABZENDA_WALLET_NOT_FOUND

    def fazenda_vazia(self, apelido: str, **kwargs) -> str:
        return "Minha Fabzenda", MSG.TEMPLATE_FABZENDA_FAZENDA_VAZIA.format(apelido=apelido)

    def fazenda_overview(self, user_animals: list[UserAnimalEntity], user: UserEntity, **kwargs) -> str:
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

        return "Fabzenda 🏕️", MSG.TEMPLATE_FABZENDA_FAZENDA.format(
            apelido=user.apelido, slots=" ".join(slots_fabzenda), animals=animals_text
        )

    def celeiro_overview(self, animal_types: list[UserAnimalEntity], balance: int, **kwargs) -> str:
        animals_text = ""
        for animal in animal_types:
            animals_text += MSG.TEMPLATE_FABZENDA_CELEIRO_ANIMAL.format(
                id=animal.type_id,
                name=animal.name,
                emoji=animal.emoji,
                price=animal.base_price,
                description=animal.description,
            )

        return "Celeiro Canto Bão 🌾", MSG.TEMPLATE_FABZENDA_CELEIRO.format(
            balance=balance,
            animals=animals_text,
        )

    def detalhe_animal_celeiro(self, animal_type: UserAnimalEntity, **kwargs) -> str:
        return "Detalhe do Fabichinho 🌾", MSG.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_DETALHE.format(
            id=animal_type.type_id,
            name=animal_type.name,
            emoji=animal_type.emoji,
            price=animal_type.base_price,
            reward=animal_type.base_reward,
            hunger_rate=animal_type.hunger_rate,
            lifespan=animal_type.lifespan,
            description=animal_type.description,
        )

    def comprar_animal(
        self,
        user: UserEntity,
        user_animal: UserAnimalEntity,
        animal_type: AnimalTypeEntity,
        animal_modifier: AnimalModifierEntity | None,
        **kwargs,
    ) -> str:
        modifier_text = ""
        if animal_modifier:
            modifier_text = f"Seu fabichinho é `{animal_modifier.name} {animal_modifier.emoji}`\n"
            modifier_text += f": {animal_modifier.description}"
        else:
            modifier_text = "Seu fabichinho é `Normal 🌱`"
            modifier_text += ": Ele não tem nenhum modificador especial mas é muito especial para você"

        message = MSG.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_COMPRADO.format(
            apelido=user.apelido, emoji=animal_type.emoji, nome=user_animal.name, modifier=modifier_text
        )

        return "Parabéns 🎉", message

    def max_animals_reached(self, apelido, **kwargs) -> str:
        return "Celeiro Canto Bão 🌾", MSG.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_ERROR_MAX_ANIMALS.format(
            apelido=apelido,
        )

    def insufficient_balance(self, apelido, **kwargs) -> str:
        return "Celeiro Canto Bão 🌾", MSG.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_ERROR_INSUFFICIENT_BALANCE.format(
            apelido=apelido,
        )

    def animal_type_not_available(self, apelido, **kwargs) -> str:
        return "Celeiro Canto Bão 🌾", MSG.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_ERROR_UNAVAILABLE.format(
            apelido=apelido,
        )

    def transaction_error(self, apelido, **kwargs) -> str:
        return "Celeiro Canto Bão 🌾", MSG.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_NAO_COMPRADO.format(
            apelido=apelido,
        )

    def alimentar_animal(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.TEMPLATE_FABZENDA_ALIMENTAR_ANIMAL_SUCESSO.format(apelido=apelido)

    def generic_error(self, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.TEMPLATE_FABZENDA_GENERIC_ERROR
