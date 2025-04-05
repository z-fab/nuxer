from sqlalchemy import Boolean, Column, Integer, String, Text  # noqa: I001
from sqlalchemy.orm import relationship

from shared.infrastructure.db_base import Base


class AnimalTypeORM(Base):
    __tablename__ = "animal_types"
    __table_args__ = {"schema": "fabzenda"}

    type_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    emoji = Column(String(10), nullable=False)
    base_price = Column(Integer, nullable=False)
    base_reward = Column(Integer, nullable=False)
    hunger_rate = Column(Integer, nullable=False)  # Em horas
    lifespan = Column(Integer, nullable=False)  # Em dias
    available = Column(Boolean, default=True)
    description = Column(Text)

    def __str__(self) -> str:
        return f"<AnimalType (type_id={self.type_id}, name='{self.name}', rarity='{self.rarity}')>"

    def __repr__(self):
        return self.__str__()


def setup_relationships():
    from domains.fabzenda.orm.user_animal import UserAnimalORM

    AnimalTypeORM.animals = relationship(
        UserAnimalORM, foreign_keys=[UserAnimalORM.type_id], back_populates="animal_type"
    )


setup_relationships()
