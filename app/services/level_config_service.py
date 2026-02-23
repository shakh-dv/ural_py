from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import LevelConfig
from app.schemas import LevelConfigCreate, LevelConfigUpdate


def get_all(db: Session):
    return db.execute(select(LevelConfig).order_by(LevelConfig.level.asc())).scalars().all()


def get_by_level(db: Session, level: int):
    config = db.get(LevelConfig, level)
    if not config:
        raise HTTPException(404, "Level config not found")
    return config


def create(db: Session, payload: LevelConfigCreate):
    config = LevelConfig(**payload.model_dump())
    db.add(config)
    db.commit()
    db.refresh(config)
    return config


def update(db: Session, level: int, payload: LevelConfigUpdate):
    config = get_by_level(db, level)
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(config, key, value)
    db.commit()
    db.refresh(config)
    return config


def delete(db: Session, level: int):
    config = get_by_level(db, level)
    db.delete(config)
    db.commit()
    return {"message": "Level config deleted"}
