from domains.fabzenda.entities.animal_type import AnimalTypeEntity
from domains.fabzenda.orm.animal_type import AnimalTypeORM
from shared.infrastructure.db_context import DatabaseExternal


class AnimalTypeRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def get_all_available(self) -> list[AnimalTypeEntity]:
        with self._db_session() as session:
            orm = session.query(AnimalTypeORM).filter(AnimalTypeORM.available).order_by(AnimalTypeORM.base_price).all()
            if not orm:
                return []

            return [AnimalTypeEntity.model_validate(animal) for animal in orm]

    def get_animal_type_by_id(self, animal_type_id: str) -> AnimalTypeEntity | None:
        with self._db_session() as session:
            orm = session.query(AnimalTypeORM).filter(AnimalTypeORM.type_id == animal_type_id).first()
            if not orm:
                return None

            return AnimalTypeEntity.model_validate(orm)
