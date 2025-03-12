from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from models.orm.base import Base


class AnimalType(Base):
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

    # Relacionamentos
    animals = relationship("UserAnimal", back_populates="animal_type")

    def __repr__(self):
        return f"<AnimalType(type_id={self.type_id}, name='{self.name}', rarity='{self.rarity}')>"
