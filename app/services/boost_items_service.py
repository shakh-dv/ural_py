from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import BoostItem
from app.schemas import BoostItemCreate, BoostItemUpdate


def get_all(db: Session):
    return db.execute(select(BoostItem)).scalars().all()


def get_by_id(db: Session, item_id: int):
    item = db.get(BoostItem, item_id)
    if not item:
        raise HTTPException(404, "Boost item not found")
    return item


def create(db: Session, payload: BoostItemCreate):
    item = BoostItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update(db: Session, item_id: int, payload: BoostItemUpdate):
    item = get_by_id(db, item_id)
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


def delete(db: Session, item_id: int):
    item = get_by_id(db, item_id)
    db.delete(item)
    db.commit()
    return {"message": "Boost item deleted"}
