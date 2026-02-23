from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserUpdate
from app.services import users_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
def get_all(db: Session = Depends(get_db)):
    return users_service.get_all(db)


@router.get("/{user_id}")
def get_by_id(user_id: int, db: Session = Depends(get_db)):
    return users_service.get_by_id(db, user_id)


@router.put("/{user_id}")
def update(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return users_service.update_balance(db, user_id, payload)
