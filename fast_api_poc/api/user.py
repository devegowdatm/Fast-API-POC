from typing import List
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends
import schema
from models import User, get_db

router = APIRouter()


@router.get("/", response_model=List[schema.UserItems])
def users(db: Session = Depends(get_db)) -> List:
    return db.query(User).all()
