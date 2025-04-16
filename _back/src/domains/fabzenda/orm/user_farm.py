from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from shared.infrastructure.db_base import Base


class UserFarmORM(Base):
    __tablename__ = "user_farm"
    __table_args__ = {"schema": "fabzenda"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("public.users.id"))
    max_animals = Column(Integer, nullable=False, default=3)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


def setup_relationships():
    from domains.user.orm.user import UserORM

    UserFarmORM.user = relationship(UserORM, foreign_keys=[UserFarmORM.user_id], back_populates="farm")


setup_relationships()
