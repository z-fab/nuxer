from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String  # noqa: I001
from sqlalchemy.orm import relationship

from shared.infrastructure.db_base import Base


class UserAnimalORM(Base):
    __tablename__ = "user_animals"
    __table_args__ = {"schema": "fabzenda"}

    animal_id = Column(Integer, primary_key=True)
    user_id = Column(String(50), ForeignKey("public.users.id"))
    type_id = Column(Integer, ForeignKey("fabzenda.animal_types.type_id"))
    name = Column(String(100))
    purchase_date = Column(DateTime, default=datetime.now)
    last_fed = Column(DateTime, default=datetime.now)
    food_slot = Column(Integer, default=4)
    health = Column(Integer, default=4)
    expiry_date = Column(DateTime)
    is_alive = Column(Boolean, default=True)
    modifier_id = Column(Integer, ForeignKey("fabzenda.animal_modifiers.modifier_id"), nullable=True)

    def __str__(self) -> str:
        return f"<UserAnimal (animal_id={self.animal_id}, name='{self.name}', user_id='{self.user_id}')>"

    def __repr__(self):
        return self.__str__()


def setup_relationships():
    from domains.fabzenda.orm.animal_modifier import AnimalModifierORM
    from domains.fabzenda.orm.animal_type import AnimalTypeORM
    from domains.user.orm.user import UserORM

    UserAnimalORM.user = relationship(UserORM, foreign_keys=[UserAnimalORM.user_id], back_populates="animals")
    UserAnimalORM.animal_type = relationship(
        AnimalTypeORM, foreign_keys=[UserAnimalORM.type_id], back_populates="animals"
    )
    UserAnimalORM.modifier = relationship(
        AnimalModifierORM, foreign_keys=[UserAnimalORM.modifier_id], back_populates="animals"
    )


setup_relationships()
