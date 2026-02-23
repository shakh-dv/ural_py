from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import user_tasks_service

router = APIRouter(prefix="/user-tasks", tags=["user-tasks"])


@router.get("")
def get_user_tasks(userId: int, db: Session = Depends(get_db)):
    return user_tasks_service.get_user_tasks(db, userId)


@router.post("/{task_id}/start")
def start_task(task_id: int, userId: int, db: Session = Depends(get_db)):
    return user_tasks_service.start_task(db, userId, task_id)
