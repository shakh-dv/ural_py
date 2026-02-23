from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Referral, ReferralStatus, User


def get_referrals(db: Session, user_id: int):
    return db.execute(select(Referral).where(Referral.inviter_id == user_id)).scalars().all()


def get_referral_link(db: Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return {"code": user.referral_code}


def reward_referral(db: Session, referral_id: int):
    referral = db.get(Referral, referral_id)
    if not referral:
        raise HTTPException(404, "Referral not found")
    inviter = db.get(User, referral.inviter_id)
    if not inviter:
        raise HTTPException(404, "Inviter not found")

    inviter.balance += 100
    referral.reward_earned += 100
    referral.status = ReferralStatus.approved
    db.commit()
    return {"message": "Referral reward applied"}
