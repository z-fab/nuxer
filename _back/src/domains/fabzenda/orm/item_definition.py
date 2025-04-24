from sqlalchemy import Column, Integer, String, Text, Enum, JSON, text, Boolean  # noqa: I001

from shared.infrastructure.db_base import Base
from sqlalchemy.orm import relationship


class ItemDefinitionORM(Base):
    __tablename__ = "item_definitions"
    __table_args__ = {"schema": "fabzenda"}

    item_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    emoji = Column(String(5), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    effect_type = Column(
        Enum("STATE_CHANGE", "MULTIPLIER", name="effect_type_enum"),
        nullable=False,
        server_default=text("'STATE_CHANGE'"),
    )
    effect = Column(JSON)
    duration = Column(Integer, nullable=True)
    available = Column(Boolean, nullable=False, default=True)

    def __str__(self) -> str:
        return f"<ItemDefinition (item_id={self.item_id}, name='{self.name}', price={self.price})>"

    def __repr__(self):
        return self.__str__()


def setup_relationships():
    from domains.fabzenda.orm.inventory_items import InventoryItemORM

    ItemDefinitionORM.inventory_items = relationship(InventoryItemORM, back_populates="item_definition", uselist=False)


setup_relationships()
