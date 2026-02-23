from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TapUseRequest
from app.services import taps_service

router = APIRouter(prefix="/taps", tags=["taps"])


@router.get("")
def get_taps(userId: int, db: Session = Depends(get_db)):
    return taps_service.get_taps(db, userId)


@router.post("/use")
def use_taps(payload: TapUseRequest, db: Session = Depends(get_db)):
    return taps_service.use_taps(db, payload)
