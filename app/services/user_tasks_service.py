from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task, TaskStatus, User, UserTask


def get_user_tasks(db: Session, user_id: int):
    return db.execute(select(UserTask).where(UserTask.user_id == user_id)).scalars().all()


def start_task(db: Session, user_id: int, task_id: int):
    user = db.get(User, user_id)
    task = db.get(Task, task_id)
    if not user or not task:
        raise HTTPException(404, "User or task not found")

    existing = db.execute(
        select(UserTask).where(UserTask.user_id == user_id, UserTask.task_id == task_id)
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(400, "Task already started")

    user_task = UserTask(
        user_id=user_id,
        task_id=task_id,
        status=TaskStatus.completed,
        completed_at=datetime.utcnow(),
    )
    user.balance += task.reward
    db.add(user_task)
    db.commit()
    return {"message": "Task completed", "reward": task.reward}
