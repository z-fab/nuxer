from models.fabzenda.entities.animal_type_entity import AnimalTypeEntity
from models.fabzenda.orm.animal_type import AnimalType


class AnimalTypeMapper:
    @staticmethod
    def orm_to_entity(orm_animal_type: AnimalType) -> AnimalTypeEntity:
        return AnimalTypeEntity(
            type_id=orm_animal_type.type_id,
            name=orm_animal_type.name,
            emoji=orm_animal_type.emoji,
            base_price=orm_animal_type.base_price,
            base_reward=orm_animal_type.base_reward,
            hunger_rate=orm_animal_type.hunger_rate,
            lifespan=orm_animal_type.lifespan,
            available=orm_animal_type.available,
            description=orm_animal_type.description,
        )
