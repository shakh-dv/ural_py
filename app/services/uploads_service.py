import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from PIL import Image
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Upload


def create_upload(db: Session, file: UploadFile, uploads_dir: Path):
    ext = Path(file.filename).suffix.lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}:
        raise HTTPException(400, "Invalid file type")

    content = file.file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(400, "File too large")

    name = f"{uuid.uuid4()}{ext}"
    full_path = uploads_dir / name
    full_path.write_bytes(content)

    xs_name = f"{full_path.stem}-xs.webp"
    md_name = f"{full_path.stem}-md.webp"

    try:
        image = Image.open(full_path)
        image.thumbnail((200, 200))
        image.save(uploads_dir / xs_name, format="WEBP", quality=75)

        image = Image.open(full_path)
        image.thumbnail((400, 400))
        image.save(uploads_dir / md_name, format="WEBP", quality=75)
    except Exception:
        xs_name = None
        md_name = None

    upload = Upload(
        filename=name,
        size=len(content),
        mimetype=file.content_type or "application/octet-stream",
        xs_filename=xs_name,
        xs_size=(uploads_dir / xs_name).stat().st_size if xs_name else None,
        md_filename=md_name,
        md_size=(uploads_dir / md_name).stat().st_size if md_name else None,
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return upload


def list_uploads(db: Session):
    return db.execute(select(Upload).order_by(Upload.created_at.desc())).scalars().all()


def delete_upload(db: Session, upload_id: int, uploads_dir: Path):
    upload = db.get(Upload, upload_id)
    if not upload:
        raise HTTPException(404, "Upload not found")

    for fname in [upload.filename, upload.xs_filename, upload.md_filename]:
        if fname:
            file_path = uploads_dir / fname
            if file_path.exists():
                file_path.unlink()

    db.delete(upload)
    db.commit()
    return {"message": "Upload deleted"}
