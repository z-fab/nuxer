from sqlalchemy import Column, Integer, String

from .base import Base


class Config(Base):
    __tablename__ = "config"
    __table_args__ = {"schema": "public"}

    id: str = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    value: str = Column(String, nullable=False)
