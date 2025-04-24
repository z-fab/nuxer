from datetime import datetime, timedelta

from domains.fabzenda.entities.inventory_item import InventoryItemEntity
from domains.fabzenda.orm.inventory_items import InventoryItemORM
from domains.fabzenda.orm.item_definition import ItemDefinitionORM
from shared.infrastructure.db_context import DatabaseExternal


class InventoryItemRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def create_inventory_item(
        self, user_id: int, item_id: int, user_animal_id: int | None, quantity: int, duration: int | None = None
    ) -> InventoryItemEntity | None:
        with self._db_session() as session:
            orm = InventoryItemORM(
                item_id=item_id,
                user_id=user_id,
                user_animal_id=user_animal_id,
                quantity=quantity,
                equipped_at=datetime.now(),
                expired_at=datetime.now() + timedelta(days=duration) if duration else None,
            )
            session.add(orm)
            session.commit()
            return InventoryItemEntity.model_validate(orm) if orm else None

    def get_inventory_items_by_user_and_item(self, user_id: int, item_id: int) -> list[InventoryItemEntity] | None:
        with self._db_session() as session:
            orm = (
                session.query(InventoryItemORM)
                .filter(InventoryItemORM.user_id == user_id, InventoryItemORM.item_id == item_id)
                .all()
            )
            if not orm:
                return None

            return [InventoryItemEntity.model_validate(item) for item in orm]

    def get_inventory_items_with_effect_by_user(self, user_id: int, effect: str) -> list[InventoryItemEntity] | None:
        with self._db_session() as session:
            orm = (
                session.query(InventoryItemORM)
                .join(ItemDefinitionORM, InventoryItemORM.item_id == ItemDefinitionORM.item_id)
                .filter(InventoryItemORM.user_id == user_id)
                .filter(ItemDefinitionORM.effect[effect].isnot(None))
                .filter((InventoryItemORM.expired_at.is_(None)) | (InventoryItemORM.expired_at > datetime.now()))
                .all()
            )
            if not orm:
                return None

            return [InventoryItemEntity.model_validate(item) for item in orm]
