from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User


def get_level(db: Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return {"level": user.level, "xp": user.xp}


def add_xp(db: Session, user_id: int, xp: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    user.xp += xp
    while user.xp >= user.level * 100:
        user.xp -= user.level * 100
        user.level += 1
    db.commit()
    return {"level": user.level, "xp": user.xp}


def reset_xp(db: Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    user.xp = 0
    db.commit()
    return {"level": user.level, "xp": 0}
