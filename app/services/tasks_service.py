from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task, TaskType
from app.schemas import TaskCreate, TaskUpdate


def get_all(db: Session, task_type: TaskType | None, page: int, limit: int):
    query = select(Task)
    if task_type:
        query = query.where(Task.task_type == task_type)
    total = len(db.execute(query).scalars().all())
    data = db.execute(query.offset((page - 1) * limit).limit(limit)).scalars().all()
    return {"data": data, "page": page, "limit": limit, "total": total}


def get_by_id(db: Session, task_id: int):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task


def create(db: Session, payload: TaskCreate):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update(db: Session, task_id: int, payload: TaskUpdate):
    task = get_by_id(db, task_id)
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def delete(db: Session, task_id: int):
    task = get_by_id(db, task_id)
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
