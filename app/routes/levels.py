from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import levels_service

router = APIRouter(prefix="/level", tags=["level"])


@router.get("/{user_id}")
def get_level(user_id: int, db: Session = Depends(get_db)):
    return levels_service.get_level(db, user_id)


@router.post("/xp/add")
def add_xp(userId: int, xp: int, db: Session = Depends(get_db)):
    return levels_service.add_xp(db, userId, xp)


@router.post("/xp/reset")
def reset_xp(userId: int, db: Session = Depends(get_db)):
    return levels_service.reset_xp(db, userId)
