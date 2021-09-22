from typing import List
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str
    price: int

    class Config:
        orm_mode = True


class User(BaseModel):
    full_name: str
    email: str

    class Config:
        orm_mode = True


class UserItems(User):

    items_list: List[ItemBase]
