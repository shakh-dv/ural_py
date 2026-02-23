import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routes import (
    auth,
    boost_effects,
    boost_items,
    level_config,
    levels,
    raffles,
    referrals,
    tasks,
    taps,
    telegram,
    uploads,
    user_tasks,
    users,
)

app = FastAPI(title="Ural Back API")

uploads_dir = Path(os.getenv("UPLOAD_DIR", "python_fastapi/uploads/dispatch"))
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads/dispatch", StaticFiles(directory=uploads_dir), name="uploads")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello from FastAPI"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(user_tasks.router)
app.include_router(boost_items.router)
app.include_router(boost_effects.router)
app.include_router(level_config.router)
app.include_router(levels.router)
app.include_router(taps.router)
app.include_router(referrals.router)
app.include_router(raffles.router)
app.include_router(telegram.router)
app.include_router(uploads.router)
