from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Raffle, RaffleParticipant, User
from app.schemas import RaffleCreate, RaffleUpdate


def create(db: Session, payload: RaffleCreate):
    raffle = Raffle(**payload.model_dump())
    db.add(raffle)
    db.commit()
    db.refresh(raffle)
    return raffle


def get_all(db: Session):
    return db.execute(select(Raffle).order_by(Raffle.created_at.desc())).scalars().all()


def get_by_id(db: Session, raffle_id: int):
    raffle = db.get(Raffle, raffle_id)
    if not raffle:
        raise HTTPException(404, "Raffle not found")
    return raffle


def update(db: Session, raffle_id: int, payload: RaffleUpdate):
    raffle = get_by_id(db, raffle_id)
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(raffle, key, value)
    db.commit()
    db.refresh(raffle)
    return raffle


def delete(db: Session, raffle_id: int):
    raffle = get_by_id(db, raffle_id)
    db.delete(raffle)
    db.commit()
    return {"message": "Raffle deleted"}


def join(db: Session, raffle_id: int, user_id: int):
    raffle = db.get(Raffle, raffle_id)
    user = db.get(User, user_id)
    if not raffle or not user:
        raise HTTPException(404, "Raffle or user not found")
    if raffle.status.value != "ACTIVE" or datetime.utcnow() > raffle.end_date:
        raise HTTPException(400, "Raffle inactive or expired")
    if user.balance < raffle.price:
        raise HTTPException(400, "Insufficient balance")

    exists = db.execute(
        select(RaffleParticipant).where(
            RaffleParticipant.user_id == user_id,
            RaffleParticipant.raffle_id == raffle_id,
        )
    ).scalar_one_or_none()
    if exists:
        raise HTTPException(400, "Already joined")

    user.balance -= raffle.price
    db.add(RaffleParticipant(user_id=user_id, raffle_id=raffle_id))
    db.commit()
    return {"message": "Joined raffle"}


def get_participants(db: Session, raffle_id: int):
    return db.execute(select(RaffleParticipant).where(RaffleParticipant.raffle_id == raffle_id)).scalars().all()
