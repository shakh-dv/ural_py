from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import TapUseRequest


def get_taps(db: Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return {"taps": user.taps, "maxTaps": user.max_taps}


def use_taps(db: Session, payload: TapUseRequest):
    user = db.get(User, payload.userId)
    if not user:
        raise HTTPException(404, "User not found")
    if user.taps < payload.count:
        raise HTTPException(400, "Not enough taps")
    user.taps -= payload.count
    user.balance += payload.count
    db.commit()
    return {"taps": user.taps, "balance": user.balance}
