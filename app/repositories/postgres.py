from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import TaskRow
from app.repositories.base import TaskRepository
from app.schemas import Task, TaskCreate, TaskPatch


def _row_to_task(row: TaskRow) -> Task:
    return Task(
        id=row.id,
        title=row.title,
        completed=row.completed,
        created_at=row.created_at,
    )


class PostgresTaskRepository(TaskRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, payload: TaskCreate) -> Task:
        row = TaskRow(
            id=uuid4(),
            title=payload.title,
            completed=False,
            created_at=datetime.now(timezone.utc),
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return _row_to_task(row)

    def list_all(self) -> list[Task]:
        stmt = select(TaskRow).order_by(TaskRow.created_at.desc())
        rows = self._session.scalars(stmt).all()
        return [_row_to_task(row) for row in rows]

    def patch(self, task_id: UUID, payload: TaskPatch) -> Task | None:
        row = self._session.get(TaskRow, task_id)
        if row is None:
            return None
        row.completed = payload.completed
        self._session.commit()
        self._session.refresh(row)
        return _row_to_task(row)
