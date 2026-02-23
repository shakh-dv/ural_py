from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import RaffleCreate, RaffleUpdate
from app.services import raffles_service

router = APIRouter(prefix="/raffles", tags=["raffles"])


@router.post("")
def create(payload: RaffleCreate, db: Session = Depends(get_db)):
    return raffles_service.create(db, payload)


@router.get("")
def get_all(db: Session = Depends(get_db)):
    return raffles_service.get_all(db)


@router.get("/{raffle_id}")
def get_by_id(raffle_id: int, db: Session = Depends(get_db)):
    return raffles_service.get_by_id(db, raffle_id)


@router.patch("/{raffle_id}")
def update(raffle_id: int, payload: RaffleUpdate, db: Session = Depends(get_db)):
    return raffles_service.update(db, raffle_id, payload)


@router.delete("/{raffle_id}")
def delete(raffle_id: int, db: Session = Depends(get_db)):
    return raffles_service.delete(db, raffle_id)


@router.post("/{raffle_id}/join")
def join(raffle_id: int, userId: int, db: Session = Depends(get_db)):
    return raffles_service.join(db, raffle_id, userId)


@router.get("/{raffle_id}/participants")
def participants(raffle_id: int, db: Session = Depends(get_db)):
    return raffles_service.get_participants(db, raffle_id)
