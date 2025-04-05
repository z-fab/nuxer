from domains.fabzenda.entities.user_animal import UserAnimalEntity
from domains.fabzenda.orm.user_animal import UserAnimalORM
from shared.infrastructure.db_context import DatabaseExternal


class UserAnimalRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def get_user_animals_alive_by_user_id(self, user_id: str) -> list[UserAnimalEntity]:
        with self._db_session() as session:
            orm = session.query(UserAnimalORM).filter(UserAnimalORM.user_id == user_id, UserAnimalORM.is_alive).all()
            if not orm:
                return []

            return [UserAnimalEntity.model_validate(animal) for animal in orm]
