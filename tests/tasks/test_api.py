import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_task(auth_client: AsyncClient, category, user):
    response = await auth_client.post(
        "/api/v1/tasks/",
        json={
            "title": "New Task",
            "description": "New Description",
            "priority": 3,
            "due_date": "2025-01-01T00:00:00Z",
            "is_completed": False,
            "category_id": category.id,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "New Task"


@pytest.mark.asyncio
async def test_get_tasks(auth_client: AsyncClient, task):
    response = await auth_client.get(
        "/api/v1/tasks/",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == "Test Task"


@pytest.mark.asyncio
async def test_get_task(auth_client: AsyncClient, task):
    response = await auth_client.get(
        f"/api/v1/tasks/{task.id}",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Test Task"


@pytest.mark.asyncio
async def test_update_task(auth_client: AsyncClient, task):
    response = await auth_client.put(
        f"/api/v1/tasks/{task.id}", json={"title": "Updated Task"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Task"


@pytest.mark.asyncio
async def test_delete_task(auth_client: AsyncClient, task):
    response = await auth_client.delete(
        f"/api/v1/tasks/{task.id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "Task deleted"


@pytest.mark.asyncio
async def test_get_nonexistent_task(auth_client: AsyncClient):
    response = await auth_client.get(
        "/api/v1/tasks/999",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_toggle_task_completed(auth_client: AsyncClient, task):
    # Проверяем начальное состояние
    assert task.is_completed is False

    # Переключаем статус
    response = await auth_client.post(
        f"/api/v1/tasks/{task.id}/toggle-completed",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_completed"] is True

    # Переключаем снова
    response = await auth_client.post(
        f"/api/v1/tasks/{task.id}/toggle-completed",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_completed"] is False


@pytest.mark.asyncio
async def test_toggle_task_completed_with_invalid_task(auth_client: AsyncClient):
    response = await auth_client.post(
        "/api/v1/tasks/999/toggle-completed",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Task not found"
