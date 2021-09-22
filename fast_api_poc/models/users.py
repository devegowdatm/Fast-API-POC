from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    items_list = relationship("Items", back_populates="user")
