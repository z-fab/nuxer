from sqlalchemy import Column, Float, Integer, String, Text  # noqa: I001
from sqlalchemy.orm import relationship

from shared.infrastructure.db_base import Base


class AnimalModifierORM(Base):
    __tablename__ = "animal_modifiers"
    __table_args__ = {"schema": "fabzenda"}

    modifier_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    emoji = Column(String(5), nullable=False)
    description = Column(Text)
    rarity = Column(Integer, nullable=False, default=0)  # 0=comum, 1=incomum, 2=raro
    feeding_cost_multiplier = Column(Float, nullable=False, default=1.0)
    burial_cost_multiplier = Column(Float, nullable=False, default=1.0)
    hunger_rate_multiplier = Column(Float, nullable=False, default=1.0)
    expire_multiplier = Column(Float, nullable=False, default=1.0)
    reward_multiplier = Column(Float, nullable=False, default=1.0)
    lifespan_multiplier = Column(Float, nullable=False, default=1.0)
    found_coin_percentage = Column(Float, nullable=False, default=5.0)

    def __str__(self) -> str:
        return f"<Modifier (modifier_id={self.modifier_id}, name='{self.name}', rarity={self.rarity})>"

    def __repr__(self):
        return self.__str__()


def setup_relationships():
    from domains.fabzenda.orm.user_animal import UserAnimalORM

    AnimalModifierORM.animals = relationship(
        UserAnimalORM, foreign_keys=[UserAnimalORM.modifier_id], back_populates="modifier"
    )


setup_relationships()
