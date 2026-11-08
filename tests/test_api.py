import os
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

os.environ["STORAGE_BACKEND"] = "memory"
# Reset cached settings/repos when tests load
from app.config import get_settings

get_settings.cache_clear()

from app.dependencies import _memory_repository
from app.main import app


@pytest.fixture
def client() -> TestClient:
    repo = _memory_repository()
    repo._tasks.clear()
    return TestClient(app)


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_list_patch_flow(client: TestClient) -> None:
    create_resp = client.post("/api/tasks", json={"title": "Learn FastAPI"})
    assert create_resp.status_code == 201
    task = create_resp.json()
    assert task["title"] == "Learn FastAPI"
    assert task["completed"] is False
    assert "id" in task
    assert "created_at" in task

    list_resp = client.get("/api/tasks")
    assert list_resp.status_code == 200
    tasks = list_resp.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task["id"]

    patch_resp = client.patch(
        f"/api/tasks/{task['id']}",
        json={"completed": True},
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["completed"] is True


def test_empty_title_rejected(client: TestClient) -> None:
    response = client.post("/api/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_patch_unknown_task(client: TestClient) -> None:
    response = client.patch(f"/api/tasks/{uuid4()}", json={"completed": True})
    assert response.status_code == 404
