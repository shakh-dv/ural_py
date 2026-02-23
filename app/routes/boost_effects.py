from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import boost_effects_service

router = APIRouter(prefix="/boost-effects", tags=["boost-effects"])


@router.post("/{item_id}/purchase")
def purchase(item_id: int, userId: int, db: Session = Depends(get_db)):
    return boost_effects_service.purchase(db, item_id, userId)
