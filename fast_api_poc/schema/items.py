import dataclasses
from pydantic import BaseModel, validator

from .users import User

# Shared properties
class ItemBase(BaseModel):
    name: str
    description: str
    price: int

    @validator('name')
    def _name(cls, v):
        if v.isdigit():
            raise ValueError('must be alphabatics')
        return v

    class Config:
        orm_mode = True


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class Items(ItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class ItemUser(ItemBase):

    user: User

    class config:
        orm_mode = True
