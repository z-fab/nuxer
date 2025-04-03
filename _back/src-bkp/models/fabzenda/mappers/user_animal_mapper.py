from models.fabzenda.entities.user_animal_entity import UserAnimalEntity
from models.fabzenda.orm.user_animal import UserAnimal


class UserAnimalMapper:
    DICT_HEALTH = {4: "Saudável 🥰", 3: "Faminto 🫠", 2: "Desnutrido 😞", 1: "Doente 😵‍💫", 0: "Morto 💀"}

    @staticmethod
    def orm_to_entity(orm_user_animal: UserAnimal) -> UserAnimalEntity:
        return UserAnimalEntity(
            animal_id=orm_user_animal.animal_id,
            user_id=orm_user_animal.user_id,
            user_entity=None,
            type_id=orm_user_animal.type_id,
            animal_type=None,
            name=orm_user_animal.name,
            purchase_date=orm_user_animal.purchase_date,
            last_fed=orm_user_animal.last_fed,
            food_slot=orm_user_animal.food_slot,
            health=orm_user_animal.health,
            health_str=UserAnimalMapper.DICT_HEALTH[orm_user_animal.health],
            expiry_date=orm_user_animal.expiry_date,
            is_alive=orm_user_animal.is_alive,
            modifier_id=orm_user_animal.modifier_id,
        )
