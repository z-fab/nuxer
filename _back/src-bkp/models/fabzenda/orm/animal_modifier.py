from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.orm import relationship

from models.orm.base import Base


class AnimalModifier(Base):
    __tablename__ = "animal_modifiers"
    __table_args__ = {"schema": "fabzenda"}

    modifier_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    emoji = Column(String(5), nullable=False)
    description = Column(Text)
    rarity = Column(Integer, nullable=False)  # 0=comum, 1=incomum, 2=raro
    feeding_cost_multiplier = Column(Float, nullable=False, default=1.0)
    burial_cost_multiplier = Column(Float, nullable=False, default=1.0)
    hunger_rate_multiplier = Column(Float, nullable=False, default=1.0)
    expire_multiplier = Column(Float, nullable=False, default=1.0)
    reward_multiplier = Column(Float, nullable=False, default=1.0)
    lifespan_multiplier = Column(Float, nullable=False, default=1.0)
    found_coin_percentage = Column(Float, nullable=False, default=5.0)

    # Relacionamento
    animals = relationship("UserAnimal", back_populates="modifier")

    def __repr__(self):
        return f"<Modifier(modifier_id={self.modifier_id}, name='{self.name}', rarity={self.rarity})>"
