from datetime import datetime
from enum import Enum

from sqlalchemy import BigInteger, DateTime, Enum as SAEnum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class ReferralStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class TaskType(str, Enum):
    click = "click"
    subscribe = "subscribe"
    external = "external"


class TaskStatus(str, Enum):
    pending = "pending"
    inProgress = "inProgress"
    completed = "completed"
    failed = "failed"


class RaffleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    COMPLETED = "COMPLETED"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String)
    avatar: Mapped[str | None] = mapped_column(String, nullable=True)
    balance: Mapped[int] = mapped_column(Integer, default=0)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    max_taps: Mapped[int] = mapped_column(Integer, default=500)
    taps: Mapped[int] = mapped_column(Integer, default=500)
    last_tap_regen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    referral_code: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Upload(Base):
    __tablename__ = "uploads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String)
    size: Mapped[int] = mapped_column(Integer)
    mimetype: Mapped[str] = mapped_column(String)
    xs_filename: Mapped[str | None] = mapped_column("xsFilename", String, nullable=True)
    xs_size: Mapped[int | None] = mapped_column("xsSize", Integer, nullable=True)
    md_filename: Mapped[str | None] = mapped_column("mdFilename", String, nullable=True)
    md_size: Mapped[int | None] = mapped_column("mdSize", Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column("created_at", DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    reward: Mapped[int] = mapped_column(Integer)
    link: Mapped[str | None] = mapped_column(String, nullable=True)
    task_type: Mapped[TaskType] = mapped_column(SAEnum(TaskType), default=TaskType.click)
    status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus), default=TaskStatus.pending)
    image_id: Mapped[int | None] = mapped_column(ForeignKey("uploads.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserTask(Base):
    __tablename__ = "user_tasks"
    __table_args__ = (UniqueConstraint("user_id", "task_id", name="user_tasks_user_id_task_id_key"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus), default=TaskStatus.pending)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Referral(Base):
    __tablename__ = "referrals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inviter_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    invitee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    reward_earned: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[ReferralStatus] = mapped_column(SAEnum(ReferralStatus), default=ReferralStatus.pending)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LevelConfig(Base):
    __tablename__ = "level_config"

    level: Mapped[int] = mapped_column(Integer, primary_key=True)
    max_energy: Mapped[int] = mapped_column(Integer)
    tap_count: Mapped[int] = mapped_column(Integer, default=1)


class BoostItem(Base):
    __tablename__ = "boost_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    cost: Mapped[int] = mapped_column(Integer)
    active: Mapped[bool] = mapped_column(default=True)
    effect_type: Mapped[str] = mapped_column(String)
    effect_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ActiveBoost(Base):
    __tablename__ = "active_boosts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    effect_type: Mapped[str] = mapped_column(String)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserBonus(Base):
    __tablename__ = "user_bonus"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[str] = mapped_column(String)


class Raffle(Base):
    __tablename__ = "raffles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[int] = mapped_column(Integer)
    image_id: Mapped[int | None] = mapped_column(ForeignKey("uploads.id"), nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[RaffleStatus] = mapped_column(SAEnum(RaffleStatus), default=RaffleStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RaffleParticipant(Base):
    __tablename__ = "raffle_participants"
    __table_args__ = (UniqueConstraint("user_id", "raffle_id", name="raffle_participants_user_id_raffle_id_key"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    raffle_id: Mapped[int] = mapped_column(ForeignKey("raffles.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
