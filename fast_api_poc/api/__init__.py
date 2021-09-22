from fastapi import APIRouter

from . import items
from .import user

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["Items Router"])
api_router.include_router(user.router, prefix="/users", tags=["User Router"])
