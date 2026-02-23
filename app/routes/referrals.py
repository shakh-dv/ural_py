from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import referrals_service

router = APIRouter(prefix="/referrals", tags=["referrals"])


@router.get("/{user_id}")
def get_referrals(user_id: int, db: Session = Depends(get_db)):
    return referrals_service.get_referrals(db, user_id)


@router.get("/referral-link")
def get_referral_link(userId: int, db: Session = Depends(get_db)):
    return referrals_service.get_referral_link(db, userId)


@router.post("/reward/{referral_id}")
def reward(referral_id: int, db: Session = Depends(get_db)):
    return referrals_service.reward_referral(db, referral_id)
