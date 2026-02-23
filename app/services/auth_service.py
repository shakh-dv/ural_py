import hashlib
import hmac
import os
import time
import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Referral, ReferralStatus, User
from app.schemas import TelegramLoginRequest

_AUTH_MAX_AGE_SECONDS = 60 * 60


def _build_data_check_string(payload: TelegramLoginRequest) -> str:
    data = payload.model_dump(exclude_none=True, by_alias=False)
    data.pop("hash", None)
    return "\n".join(f"{key}={value}" for key, value in sorted(data.items()))


def _verify_telegram_login_data(payload: TelegramLoginRequest) -> None:
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise HTTPException(500, "TELEGRAM_BOT_TOKEN is not configured")

    now = int(time.time())
    if payload.auth_date > now + 5 or now - payload.auth_date > _AUTH_MAX_AGE_SECONDS:
        raise HTTPException(401, "Telegram login data is expired")

    secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()
    check_string = _build_data_check_string(payload)
    expected_hash = hmac.new(secret_key, check_string.encode("utf-8"), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected_hash, payload.hash):
        raise HTTPException(401, "Invalid Telegram login data")


def login(db: Session, payload: TelegramLoginRequest, startapp: str | None):
    _verify_telegram_login_data(payload)

    user = db.execute(select(User).where(User.telegram_id == payload.id)).scalar_one_or_none()
    if user is None:
        user = User(
            telegram_id=payload.id,
            first_name=payload.first_name,
            username=payload.username,
            avatar=payload.photo_url,
            referral_code=str(uuid.uuid4()),
        )
        db.add(user)
        db.flush()

    if startapp and startapp != user.referral_code:
        inviter = db.execute(select(User).where(User.referral_code == startapp)).scalar_one_or_none()
        if inviter:
            exists = db.execute(
                select(Referral).where(
                    Referral.inviter_id == inviter.id,
                    Referral.invitee_id == user.id,
                )
            ).scalar_one_or_none()
            if exists is None:
                db.add(
                    Referral(
                        inviter_id=inviter.id,
                        invitee_id=user.id,
                        status=ReferralStatus.pending,
                    )
                )

    db.commit()
    return {"userId": user.id}
