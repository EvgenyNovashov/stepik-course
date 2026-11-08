from pathlib import Path
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.db import init_db
from app.dependencies import get_task_repository
from app.repositories.base import TaskRepository
from app.schemas import Task, TaskCreate, TaskPatch

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


def create_app() -> FastAPI:
    application = FastAPI(title="Task Tracker", version="0.1.0")

    @application.on_event("startup")
    def on_startup() -> None:
        settings = get_settings()
        if settings.storage_backend == "postgres":
            init_db()

    @application.get("/health")
    def health() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    @application.post("/api/tasks", response_model=Task, status_code=201)
    def create_task(
        payload: TaskCreate,
        repo: TaskRepository = Depends(get_task_repository),
    ) -> Task:
        return repo.create(payload)

    @application.get("/api/tasks", response_model=list[Task])
    def list_tasks(
        repo: TaskRepository = Depends(get_task_repository),
    ) -> list[Task]:
        return repo.list_all()

    @application.patch("/api/tasks/{task_id}", response_model=Task)
    def patch_task(
        task_id: UUID,
        payload: TaskPatch,
        repo: TaskRepository = Depends(get_task_repository),
    ) -> Task:
        updated = repo.patch(task_id, payload)
        if updated is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated

    if FRONTEND_DIR.is_dir():
        application.mount(
            "/",
            StaticFiles(directory=str(FRONTEND_DIR), html=True),
            name="frontend",
        )

    return application


app = create_app()
