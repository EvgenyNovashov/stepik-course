from collections.abc import Generator
from functools import lru_cache

from app.config import get_settings
from app.db import get_session, init_db
from app.repositories.base import TaskRepository
from app.repositories.memory import InMemoryTaskRepository
from app.repositories.postgres import PostgresTaskRepository


@lru_cache
def _memory_repository() -> InMemoryTaskRepository:
    return InMemoryTaskRepository()


def get_task_repository() -> Generator[TaskRepository, None, None]:
    settings = get_settings()
    if settings.storage_backend == "memory":
        yield _memory_repository()
        return

    init_db()
    session_gen = get_session()
    session = next(session_gen)
    try:
        yield PostgresTaskRepository(session)
    finally:
        session.close()
