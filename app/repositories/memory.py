from datetime import datetime, timezone
from threading import Lock
from uuid import UUID, uuid4

from app.repositories.base import TaskRepository
from app.schemas import Task, TaskCreate, TaskPatch


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._tasks: dict[UUID, Task] = {}
        self._lock = Lock()

    def create(self, payload: TaskCreate) -> Task:
        task = Task(
            id=uuid4(),
            title=payload.title,
            completed=False,
            created_at=datetime.now(timezone.utc),
        )
        with self._lock:
            self._tasks[task.id] = task
        return task

    def list_all(self) -> list[Task]:
        with self._lock:
            tasks = list(self._tasks.values())
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

    def patch(self, task_id: UUID, payload: TaskPatch) -> Task | None:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return None
            updated = task.model_copy(update={"completed": payload.completed})
            self._tasks[task_id] = updated
            return updated
