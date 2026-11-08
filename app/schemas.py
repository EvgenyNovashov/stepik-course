from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("title must not be empty")
        return stripped


class TaskPatch(BaseModel):
    completed: bool


class Task(BaseModel):
    id: UUID
    title: str
    completed: bool
    created_at: datetime
