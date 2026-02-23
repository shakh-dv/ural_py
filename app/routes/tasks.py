from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TaskType
from app.schemas import TaskCreate, TaskUpdate
from app.services import tasks_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
def get_all(taskType: TaskType | None = None, page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    return tasks_service.get_all(db, taskType, page, limit)


@router.get("/{task_id}")
def get_by_id(task_id: int, db: Session = Depends(get_db)):
    return tasks_service.get_by_id(db, task_id)


@router.post("")
def create(payload: TaskCreate, db: Session = Depends(get_db)):
    return tasks_service.create(db, payload)


@router.patch("/{task_id}")
def update(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    return tasks_service.update(db, task_id, payload)


@router.delete("/{task_id}")
def delete(task_id: int, db: Session = Depends(get_db)):
    return tasks_service.delete(db, task_id)
