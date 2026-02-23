from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import BoostItemCreate, BoostItemUpdate
from app.services import boost_items_service

router = APIRouter(prefix="/boost-items", tags=["boost-items"])


@router.get("")
def get_all(db: Session = Depends(get_db)):
    return boost_items_service.get_all(db)


@router.get("/{item_id}")
def get_by_id(item_id: int, db: Session = Depends(get_db)):
    return boost_items_service.get_by_id(db, item_id)


@router.post("")
def create(payload: BoostItemCreate, db: Session = Depends(get_db)):
    return boost_items_service.create(db, payload)


@router.patch("/{item_id}")
def update(item_id: int, payload: BoostItemUpdate, db: Session = Depends(get_db)):
    return boost_items_service.update(db, item_id, payload)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return boost_items_service.delete(db, item_id)
