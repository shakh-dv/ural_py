from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import LevelConfigCreate, LevelConfigUpdate
from app.services import level_config_service

router = APIRouter(prefix="/level-config", tags=["level-config"])


@router.get("")
def get_all(db: Session = Depends(get_db)):
    return level_config_service.get_all(db)


@router.get("/{level}")
def get_by_level(level: int, db: Session = Depends(get_db)):
    return level_config_service.get_by_level(db, level)


@router.post("")
def create(payload: LevelConfigCreate, db: Session = Depends(get_db)):
    return level_config_service.create(db, payload)


@router.patch("/{level}")
def update(level: int, payload: LevelConfigUpdate, db: Session = Depends(get_db)):
    return level_config_service.update(db, level, payload)


@router.delete("/{level}")
def delete(level: int, db: Session = Depends(get_db)):
    return level_config_service.delete(db, level)
