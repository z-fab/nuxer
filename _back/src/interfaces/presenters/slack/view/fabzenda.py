from datetime import datetime

from domains.fabzenda import messages as MSG
from domains.fabzenda.entities.animal_modifier import AnimalModifierEntity
from domains.fabzenda.entities.animal_type import AnimalTypeEntity
from domains.fabzenda.entities.user_animal import UserAnimalEntity
from domains.user.entities.user import UserEntity


class FabzendaSlackPresenter:
    def __init__(self, now: datetime | None = None):
        self.now = now or datetime.now()

    def fazenda_overview_vazia(self, apelido: str, **kwargs) -> str:
        return "Minha Fabzenda", MSG.FAZENDA_OVERVIEW_VAZIA.format(apelido=apelido)

    def fazenda_overview(self, user_animals: list[UserAnimalEntity], user: UserEntity, **kwargs) -> str:
        slots_fabzenda = [f"{animal.animal_type.emoji}" for animal in user_animals]

        animals_text = ""
        for animal in user_animals:
            # Verificando se o animal está morto
            if animal.health == 0:
                animals_text += MSG.FAZENDA_OVERVIEW_ANIMAL_DEAD.format(
                    emoji=animal.animal_type.emoji,
                    burial_cost=animal.burial_cost,
                    type=animal.animal_type.name,
                    name=animal.name,
                    health=animal.health_str,
                    id=animal.animal_id,
                )
                continue

            # Verificando se o animal foi Abduzido
            if (animal.expiry_date <= datetime.now()) or (animal.health == -1):
                animals_text += MSG.FAZENDA_OVERVIEW_ANIMAL_ABDUZIDO.format(
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

            animals_text += MSG.FAZENDA_OVERVIEW_ANIMALS.format(
                emoji=animal.animal_type.emoji,
                type=animal.animal_type.name,
                name=animal.name,
                reward=animal.reward,
                expire_value=animal.expire_value,
                modifier=f"{animal.modifier.name} {animal.modifier.emoji}" if animal.modifier else "Normal 🌱",
                health=animal.health_str,
                hunger=hunger,
                age=f"{age} dias" if age > 1 else f"{age} dia" if age == 1 else "Recém-nascido",
                feeding_cost=animal.feeding_cost,
                id=animal.animal_id,
                primary="P" if (animal.food_slot == 0 or animal.health < 4) else "",
            )

        return "Fabzenda 🏕️", MSG.FAZENDA_OVERVIEW.format(
            apelido=user.apelido, slots=" ".join(slots_fabzenda), animals=animals_text
        )

    def fazenda_overview_detalhe_animal(self, user_animal: UserAnimalEntity, **kwargs) -> str:
        animals_text = ""

        if user_animal.health == 0:
            animals_text = MSG.FAZENDA_OVERVIEW_ANIMAL_DEAD.format(
                emoji=user_animal.animal_type.emoji,
                burial_cost=user_animal.burial_cost,
                type=user_animal.animal_type.name,
                name=user_animal.name,
                health=user_animal.health_str,
                id=user_animal.animal_id,
            )

        # Verificando se o animal foi Abduzido

        elif (user_animal.expiry_date <= datetime.now()) or (user_animal.health == -1):
            animals_text = MSG.FAZENDA_OVERVIEW_ANIMAL_ABDUZIDO.format(
                emoji=user_animal.animal_type.emoji,
                expire_value=user_animal.expire_value,
                type=user_animal.animal_type.name,
                name=user_animal.name,
                id=user_animal.animal_id,
            )
        else:
            food_slot_full = " `🍔` " * user_animal.food_slot
            food_slot_empty = " `‧` " * (4 - user_animal.food_slot)
            hunger = f"{food_slot_full}{food_slot_empty}"

            age = (datetime.now() - user_animal.purchase_date).days

            map_health_description = {
                4: MSG.FAZENDA_OVERVIEW_ANIMAL_HEALTH_4,
                3: MSG.FAZENDA_OVERVIEW_ANIMAL_HEALTH_3,
                2: MSG.FAZENDA_OVERVIEW_ANIMAL_HEALTH_2,
                1: MSG.FAZENDA_OVERVIEW_ANIMAL_HEALTH_1,
            }
            health_description = map_health_description.get(user_animal.health, MSG.FAZENDA_OVERVIEW_ANIMAL_HEALTH_4)

            animals_text = MSG.FAZENDA_OVERVIEW_ANIMALS_DETAIL.format(
                emoji=user_animal.animal_type.emoji,
                type=user_animal.animal_type.name,
                name=user_animal.name,
                reward=user_animal.reward,
                expire_value=user_animal.expire_value,
                modifier=f"{user_animal.modifier.name} {user_animal.modifier.emoji}"
                if user_animal.modifier
                else "Normal 🌱",
                modifier_description=user_animal.modifier.resume_modifier
                if user_animal.modifier
                else "Seu fabichinho é normal (mas continua especial)",
                health=user_animal.health_str,
                health_description=health_description,
                hunger=hunger,
                hunger_rate=user_animal.hunger_rate,
                age=f"{age} dias" if age > 1 else f"{age} dia" if age == 1 else "Recém-nascido",
                lifespan=user_animal.lifespan,
                feeding_cost=user_animal.feeding_cost,
                id=user_animal.animal_id,
                primary="P" if (user_animal.food_slot == 0 or user_animal.health < 4) else "",
            )

        return "Fabzenda 🏕️", animals_text

    def celeiro_overview(self, animal_types: list[UserAnimalEntity], balance: int, **kwargs) -> str:
        animals_text = ""
        for animal in animal_types:
            animals_text += MSG.CELEIRO_OVERVIEW_ANIMALS.format(
                id=animal.type_id,
                name=animal.name,
                emoji=animal.emoji,
                price=animal.base_price,
                description=animal.description,
            )

        return "Celeiro Canto Bão 🌾", MSG.CELEIRO_OVERVIEW.format(
            balance=balance,
            animals=animals_text,
        )

    def celeiro_detalhe_animal(self, animal_type: UserAnimalEntity, **kwargs) -> str:
        return "Detalhe do Fabichinho 🌾", MSG.CELEIRO_ANIMAL_DETAIL.format(
            id=animal_type.type_id,
            name=animal_type.name,
            emoji=animal_type.emoji,
            price=animal_type.base_price,
            reward=animal_type.base_reward,
            hunger_rate=animal_type.hunger_rate,
            lifespan=animal_type.lifespan,
            description=animal_type.description,
        )

    def celeiro_max_animals_reached(self, apelido, **kwargs) -> str:
        return "Celeiro Canto Bão 🌾", MSG.CELEIRO_ANIMAL_DETAIL_MAX_REACHED.format(
            apelido=apelido,
        )

    def celeiro_insufficient_balance(self, apelido, **kwargs) -> str:
        return "Celeiro Canto Bão 🌾", MSG.CELEIRO_ANIMAL_DETAIL_INSUFFICIENT_BALANCE.format(
            apelido=apelido,
        )

    def celeiro_animal_type_not_available(self, apelido, **kwargs) -> str:
        return "Celeiro Canto Bão 🌾", MSG.CELEIRO_ANIMAL_DETAIL_NOT_AVAILABLE.format(
            apelido=apelido,
        )

    def celeiro_transaction_error(self, apelido, **kwargs) -> str:
        return "Celeiro Canto Bão 🌾", MSG.CELEIRO_ANIMAL_DETAIL_TRANSACTION_ERROR.format(
            apelido=apelido,
        )

    def celeiro_created_error(self, apelido, **kwargs) -> str:
        return "Celeiro Canto Bão 🌾", MSG.CELEIRO_ANIMAL_DETAIL_CREATED_ERROR.format(
            apelido=apelido,
        )

    def celeiro_wallet_not_found(self, **kwargs) -> str:
        return "Canto Bão 🌾", MSG.CELEIRO_ANIMAL_DETAIL_WALLET_NOT_FOUND

    def celeiro_compra_animal(
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

        message = MSG.CELEIRO_ANIMAL_DETAIL_BUY_SUCCESS.format(
            apelido=user.apelido, emoji=animal_type.emoji, nome=user_animal.name, modifier=modifier_text
        )

        return "Parabéns 🎉", message

    #####

    def alimentar_animal(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.FEED_SUCCESS.format(apelido=apelido)

    def alimentar_insufficient_balance(self, apelido, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.FEED_INSUFFICIENT_BALANCE.format(
            apelido=apelido,
        )

    def alimentar_animal_dead(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.FEED_ANIMAL_DEAD.format(apelido=apelido)

    def alimentar_transaction_error(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.FEED_TRANSACTION_ERROR.format(apelido=apelido)

    def alimentar_error(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.FEED_ERROR.format(apelido=apelido)

    ####

    def enterrar_animal(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.BURIAL_SUCCESS.format(apelido=apelido)

    def enterrar_insufficient_balance(self, apelido, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.BURIAL_INSUFFICIENT_BALANCE.format(
            apelido=apelido,
        )

    def enterrar_animal_lives(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.BURIAL_ANIMAL_LIVES.format(apelido=apelido)

    def enterrar_transaction_error(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.BURIAL_TRANSACTION_ERROR.format(apelido=apelido)

    def enterrar_error(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.BURIAL_ERROR.format(apelido=apelido)

    ####

    def abduzir_animal(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.ABDUCTION_SUCCESS.format(apelido=apelido)

    def abduzir_animal_lives(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.ABDUCTION_ANIMAL_LIVES.format(apelido=apelido)

    def abduzir_transaction_error(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.ABDUCTION_TRANSACTION_ERROR.format(apelido=apelido)

    def abduzir_error(self, apelido: str, **kwargs) -> str:
        return "Fabzenda 🏕️", MSG.ABDUCTION_ERROR.format(apelido=apelido)
