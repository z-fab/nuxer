from domains.fabbank.entities.item_loja import ItemLojaEntity
from domains.fabbank.orm.item_loja import ItemLojaORM
from shared.infrastructure.db_context import DatabaseExternal


class StoreRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def get_all_enabled_items(self) -> list[ItemLojaEntity] | list[None]:
        with self._db_session() as session:
            orm = session.query(ItemLojaORM).filter(ItemLojaORM.enable).all()
            return [ItemLojaEntity.model_validate(w) for w in orm]

    def get_item_by_cod(self, cod: str) -> ItemLojaEntity | None:
        with self._db_session() as session:
            orm = session.query(ItemLojaORM).filter(ItemLojaORM.cod == cod).first()
            if not orm:
                return None
            return ItemLojaEntity.model_validate(orm)
