from pathlib import Path
import os

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import uploads_service

router = APIRouter(prefix="/uploads", tags=["uploads"])


def _uploads_dir() -> Path:
    path = Path(os.getenv("UPLOAD_DIR", "python_fastapi/uploads/dispatch"))
    path.mkdir(parents=True, exist_ok=True)
    return path


@router.post("")
def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return uploads_service.create_upload(db, file, _uploads_dir())


@router.get("")
def get_all(db: Session = Depends(get_db)):
    return uploads_service.list_uploads(db)


@router.delete("/{upload_id}")
def delete(upload_id: int, db: Session = Depends(get_db)):
    return uploads_service.delete_upload(db, upload_id, _uploads_dir())
