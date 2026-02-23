from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserUpdate


def get_all(db: Session):
    return db.execute(select(User).order_by(User.created_at.desc())).scalars().all()


def get_by_id(db: Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


def update_balance(db: Session, user_id: int, payload: UserUpdate):
    user = get_by_id(db, user_id)
    user.balance += payload.balance
    db.commit()
    db.refresh(user)
    return user
