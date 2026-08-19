"""Integration tests for FastAPI Task Management Service."""

import pytest
from fastapi.testclient import TestClient
from main import app, TASKS_DB


@pytest.fixture(autouse=True)
def clean_db():
    TASKS_DB.clear()
    yield
    TASKS_DB.clear()


client = TestClient(app)


def test_create_and_fetch_task():
    res = client.post("/tasks", json={"title": "Write curriculum", "priority": "high"})
    assert res.status_code == 201
    task = res.json()
    assert task["id"] == 1
    assert task["title"] == "Write curriculum"
    assert task["priority"] == "high"
    assert task["completed"] is False

    # Fetch task
    get_res = client.get("/tasks/1")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Write curriculum"


def test_validation_rejection():
    # Empty title should fail with 422 Unprocessable Entity
    res = client.post("/tasks", json={"title": "", "priority": "high"})
    assert res.status_code == 422


def test_update_and_delete_flow():
    post_res = client.post("/tasks", json={"title": "Draft PR"})
    task_id = post_res.json()["id"]

    # Patch completed status
    patch_res = client.patch(f"/tasks/{task_id}", json={"completed": True})
    assert patch_res.status_code == 200
    assert patch_res.json()["completed"] is True

    # Delete task
    del_res = client.delete(f"/tasks/{task_id}")
    assert del_res.status_code == 204

    # Verify 404
    assert client.get(f"/tasks/{task_id}").status_code == 404
