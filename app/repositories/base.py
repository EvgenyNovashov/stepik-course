from abc import ABC, abstractmethod
from uuid import UUID

from app.schemas import Task, TaskCreate, TaskPatch


class TaskRepository(ABC):
    @abstractmethod
    def create(self, payload: TaskCreate) -> Task:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def patch(self, task_id: UUID, payload: TaskPatch) -> Task | None:
        raise NotImplementedError
