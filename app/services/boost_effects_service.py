from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import ActiveBoost, BoostItem, User


def purchase(db: Session, item_id: int, user_id: int):
    item = db.get(BoostItem, item_id)
    user = db.get(User, user_id)
    if not item or not user:
        raise HTTPException(404, "Boost item or user not found")
    if user.balance < item.cost:
        raise HTTPException(400, "Insufficient balance")

    user.balance -= item.cost
    expires_at = datetime.utcnow() + timedelta(minutes=item.effect_value or 60)
    db.add(ActiveBoost(user_id=user.id, effect_type=item.effect_type, expires_at=expires_at))
    db.commit()
    return {"message": "Boost applied", "effectType": item.effect_type, "expiresAt": expires_at}
