from domains.fabzenda.entities.item_definition import ItemDefinitionEntity
from domains.fabzenda.orm.item_definition import ItemDefinitionORM
from shared.infrastructure.db_context import DatabaseExternal


class ItemDefinitionRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def get_all_available(self) -> list[ItemDefinitionEntity]:
        with self._db_session() as session:
            orm = (
                session.query(ItemDefinitionORM)
                .filter(ItemDefinitionORM.available)
                .order_by(ItemDefinitionORM.item_id)
                .all()
            )
            if not orm:
                return []

            return [ItemDefinitionEntity.model_validate(item) for item in orm]

    def get_item_definition_by_id(self, item_id: int) -> ItemDefinitionEntity | None:
        with self._db_session() as session:
            orm = session.query(ItemDefinitionORM).filter(ItemDefinitionORM.item_id == item_id).first()
            if not orm:
                return None

            return ItemDefinitionEntity.model_validate(orm)
