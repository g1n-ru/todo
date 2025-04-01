from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskCreate
from app.tasks.service import TaskService


@pytest.mark.asyncio
async def test_create_task_with_invalid_priority():
    # Попытка создать задачу с недопустимым приоритетом
    mock_repo = AsyncMock(spec=TaskRepository)

    service = TaskService(repository=mock_repo)

    with pytest.raises(ValidationError):
        await service.create_task(
            TaskCreate(
                title="Invalid Task",
                description="This task has invalid priority",
                priority=10,  # Недопустимое значение
                due_date=datetime(2023, 12, 31),
                is_completed=False,
                category_id=None,
            ),
            owner_id=1,
        )


@pytest.mark.asyncio
async def test_get_nonexistent_task():
    # Мок репозитория возвращает None (задача не найдена)
    mock_repo = AsyncMock(spec=TaskRepository)
    mock_repo.get_by_id.return_value = None

    service = TaskService(repository=mock_repo)

    task = await service.get_task(task_id=999)
    assert task is None


# @pytest.mark.asyncio
# async def test_update_nonexistent_task():
#     # Мок репозитория возвращает None (задача не найдена)
#     mock_repo = AsyncMock(spec=TaskRepository)
#     mock_repo.update.return_value = None

#     service = TaskService(repository=mock_repo)

#     updated_task = await service.update_task(task_id=999, updated_data={"title": "Updated Title"})
#     assert updated_task is None


# @pytest.mark.asyncio
# async def test_delete_nonexistent_task():
#     # Мок репозитория возвращает False (задача не найдена)
#     mock_repo = AsyncMock(spec=TaskRepository)
#     mock_repo.delete.return_value = False

#     service = TaskService(repository=mock_repo)

#     success = await service.delete_task(task_id=999)
#     assert success is False
