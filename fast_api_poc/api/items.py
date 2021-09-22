from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.dialects import postgresql

from schema import (
    GenerateModelFields,
    ItemBase,
    ItemCreate,
    ItemUpdate
)
from models import Items, async_db, get_db

router = APIRouter()


# ASYNC DB END POINTS
@router.get("/async", response_model=List[ItemBase])
async def async_database(db: Session=Depends(get_db)) -> List:

    # Type 1, Use Raw query.
    query = 'select name, description, price from items'

    # Type 2 , Use Sqlalchemy table methods.
    query = Items.__table__.select()

    # Type 3, Convert Sqlalchemy query into RAW postgress query.
    query = str(db.query(Items).limit(2).statement.compile(
        dialect=postgresql.dialect(),
        compile_kwargs={"literal_binds": True})
    )

    # Non-blocking code
    data = await async_db.fetch_all(query=query)

    # Custom Logic to parse data to map data to pydantic model.
    base_data = []
    for _d in data:
        _t = GenerateModelFields(ItemBase)
        _t.set_fields(_d)
        base_data.append(_t)

    return base_data


@router.post("async/{user_id}", response_model=ItemBase)
async def create_items(user_id: int, schema_model: ItemCreate) -> Dict:

    query = Items.__table__.insert().values(
        **schema_model.dict(),
        user_id=user_id,
        created_at=datetime.utcnow()
    )

    await async_db.execute(query)
    return {**schema_model.dict()}


# SYNC DB END POINTS.
@router.get("/", response_model=List[ItemBase])
async def items(db: Session=Depends(get_db)) -> List:
    return db.query(Items).all()


@router.get("/{item_id}", response_model=ItemBase)
async def get_item(item_id: int, db: Session=Depends(get_db)):
    return db.query(Items).get(item_id)


@router.post("/create-item/{user_id}/", response_model=ItemBase)
async def create_item_for_user(
    user_id: int, schema_model: ItemCreate, db: Session=Depends(get_db)
):

    db_item = Items(**schema_model.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/edit-item/{item_id}", response_model=ItemBase)
async def update_item_for_user(
    item_id: int, schema_model: ItemUpdate, db: Session=Depends(get_db)
):

    db_item = db.query(Items).get(item_id)

    obj_data = jsonable_encoder(db_item)
    if isinstance(schema_model, dict):
        update_data = schema_model
    else:
        update_data = schema_model.dict(exclude_unset=True)

    for field in obj_data:
        if field in update_data:
            setattr(db_item, field, update_data[field])

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
