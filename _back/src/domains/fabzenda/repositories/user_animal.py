from datetime import datetime, timedelta

from domains.fabzenda.entities.user_animal import UserAnimalEntity
from domains.fabzenda.orm.user_animal import UserAnimalORM
from shared.infrastructure.db_context import DatabaseExternal


class UserAnimalRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def get_user_animal_by_id(self, user_animal_id: str) -> UserAnimalEntity | None:
        with self._db_session() as session:
            orm = session.query(UserAnimalORM).filter(UserAnimalORM.animal_id == user_animal_id).first()
            if not orm:
                return None

            return UserAnimalEntity.model_validate(orm)

    def get_user_animals_alive_by_user_id(self, user_id: str) -> list[UserAnimalEntity]:
        with self._db_session() as session:
            orm = session.query(UserAnimalORM).filter(UserAnimalORM.user_id == user_id, UserAnimalORM.is_alive).all()
            if not orm:
                return []

            return [UserAnimalEntity.model_validate(animal) for animal in orm]

    def create_user_animal(
        self, user_id: str, animal_type_id: str, lifespan: int, id_modifier: int | None, nickname: str
    ) -> UserAnimalEntity | None:
        with self._db_session() as session:
            orm = UserAnimalORM(
                user_id=user_id,
                type_id=animal_type_id,
                modifier_id=id_modifier,
                name=nickname,
                purchase_date=datetime.now(),
                last_fed=datetime.now(),
                expiry_date=datetime.now() + timedelta(days=lifespan),
            )
            session.add(orm)
            session.commit()
            return UserAnimalEntity.model_validate(orm) if orm else None

    def update_user_animal(self, user_animal: UserAnimalEntity) -> UserAnimalEntity | None:
        with self._db_session() as session:
            orm = session.query(UserAnimalORM).filter(UserAnimalORM.animal_id == user_animal.animal_id).first()
            if not orm:
                return None

            orm.name = user_animal.name
            orm.last_fed = user_animal.last_fed
            orm.expiry_date = user_animal.expiry_date
            orm.is_alive = user_animal.is_alive
            orm.user_id = user_animal.user_id
            orm.type_id = user_animal.type_id
            orm.food_slot = user_animal.food_slot
            orm.health = user_animal.health
            orm.modifier_id = user_animal.modifier_id

            session.commit()

            return UserAnimalEntity.model_validate(orm)
