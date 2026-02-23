from datetime import datetime
from typing import Any

from pydantic import BaseModel

from .models import RaffleStatus, ReferralStatus, TaskStatus, TaskType


class UserUpdate(BaseModel):
    balance: int = 0


class TaskCreate(BaseModel):
    title: str
    description: str
    reward: int
    link: str | None = None
    task_type: TaskType = TaskType.click
    status: TaskStatus = TaskStatus.pending
    image_id: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    reward: int | None = None
    link: str | None = None
    task_type: TaskType | None = None
    status: TaskStatus | None = None
    image_id: int | None = None


class BoostItemCreate(BaseModel):
    title: str
    description: str | None = None
    cost: int
    active: bool = True
    effect_type: str
    effect_value: int | None = None


class BoostItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    cost: int | None = None
    active: bool | None = None
    effect_type: str | None = None
    effect_value: int | None = None


class LevelConfigCreate(BaseModel):
    level: int
    max_energy: int
    tap_count: int = 1


class LevelConfigUpdate(BaseModel):
    max_energy: int | None = None
    tap_count: int | None = None


class RaffleCreate(BaseModel):
    title: str
    description: str | None = None
    price: int
    image_id: int | None = None
    end_date: datetime
    status: RaffleStatus = RaffleStatus.ACTIVE


class RaffleUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    image_id: int | None = None
    end_date: datetime | None = None
    status: RaffleStatus | None = None


class TelegramLoginRequest(BaseModel):
    id: int
    first_name: str
    auth_date: int
    hash: str
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None


class TapUseRequest(BaseModel):
    userId: int
    count: int = 1


class GenericMessage(BaseModel):
    message: str
    payload: dict[str, Any] | None = None
