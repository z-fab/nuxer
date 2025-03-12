from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from models.orm.base import Base


class UserAnimal(Base):
    __tablename__ = "user_animals"
    __table_args__ = {"schema": "fabzenda"}

    animal_id = Column(Integer, primary_key=True)
    user_id = Column(String(50), ForeignKey("public.users.id"))
    type_id = Column(Integer, ForeignKey("fabzenda.animal_types.type_id"))
    name = Column(String(100))
    purchase_date = Column(DateTime, default=func.current_timestamp())
    last_fed = Column(DateTime, default=func.current_timestamp())
    food_slot = Column(Integer, default=4)
    health = Column(Integer, default=4)
    expiry_date = Column(DateTime)
    is_alive = Column(Boolean, default=True)
    modifier_id = Column(Integer, ForeignKey("fabzenda.animal_modifiers.modifier_id"), nullable=True)

    # Relacionamentos
    user = relationship("User", back_populates="animals")
    animal_type = relationship("AnimalType", back_populates="animals")
    modifier = relationship("AnimalModifier", back_populates="animals")

    def __repr__(self):
        return f"<UserAnimal(animal_id={self.animal_id}, name='{self.name}', user_id='{self.user_id}')>"
