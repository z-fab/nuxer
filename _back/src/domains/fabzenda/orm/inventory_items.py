from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer  # noqa: I001
from sqlalchemy.orm import relationship

from shared.infrastructure.db_base import Base


class InventoryItemORM(Base):
    __tablename__ = "inventory_items"
    __table_args__ = {"schema": "fabzenda"}

    inventory_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("fabzenda.item_definitions.item_id"))
    user_id = Column(Integer, ForeignKey("public.users.id"))
    user_animal_id = Column(Integer, ForeignKey("fabzenda.user_animals.animal_id"))
    quantity = Column(Integer, default=1)
    equipped_at = Column(DateTime, default=datetime.now)
    expired_at = Column(DateTime, nullable=True)

    def __str__(self) -> str:
        return (
            f"<InventoryItems (inventory_id={self.inventory_id}, item_id='{self.item_id}', user_id='{self.user_id}')>"
        )

    def __repr__(self):
        return self.__str__()


def setup_relationships():
    from domains.fabzenda.orm.item_definition import ItemDefinitionORM
    from domains.fabzenda.orm.user_animal import UserAnimalORM
    from domains.user.orm.user import UserORM

    InventoryItemORM.item_definition = relationship(
        ItemDefinitionORM, foreign_keys=[InventoryItemORM.item_id], back_populates="inventory_items"
    )
    InventoryItemORM.user = relationship(
        UserORM, foreign_keys=[InventoryItemORM.user_id], back_populates="inventory_items"
    )
    InventoryItemORM.user_animal = relationship(
        UserAnimalORM, foreign_keys=[InventoryItemORM.user_animal_id], back_populates="inventory_items"
    )


setup_relationships()
