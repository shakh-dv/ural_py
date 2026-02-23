from fastapi import APIRouter

from app.services import telegram_service

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/extract-link")
def extract_link(link: str):
    return telegram_service.extract_chat_id(link)
