from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.types import Date
from .base import Base
from sqlalchemy.orm import relationship


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    created_at = Column(Date, default=datetime.utcnow, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship('User', back_populates="items_list")
