from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TelegramLoginRequest
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(payload: TelegramLoginRequest, startapp: str | None = Query(default=None), db: Session = Depends(get_db)):
    return auth_service.login(db, payload, startapp)
