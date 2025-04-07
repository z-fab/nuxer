from domains.fabzenda.entities.animal_modifier import AnimalModifierEntity
from domains.fabzenda.orm.animal_modifier import AnimalModifierORM
from shared.infrastructure.db_context import DatabaseExternal


class AnimalModifierRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def get_modifier_by_rarity(self, rarity: int) -> list[AnimalModifierEntity]:
        with self._db_session() as session:
            orm = session.query(AnimalModifierORM).filter(AnimalModifierORM.rarity == rarity).all()
            if not orm:
                return []

            return [AnimalModifierEntity.model_validate(modifier) for modifier in orm]
