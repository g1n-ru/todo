from datetime import datetime

import pytest

from app.tasks.repository import TaskRepository


@pytest.mark.asyncio
async def test_create_task(db_session, user, category):
    repo = TaskRepository(db_session)
    task = await repo.create(
        title="Finish project",
        description="Complete the backend part",
        priority=3,
        due_date=datetime(2023, 12, 31),
        is_completed=False,
        owner_id=user.id,
        category_id=category.id,
    )

    assert task.title == "Finish project"
    assert task.priority == 3
    assert task.is_completed is False


@pytest.mark.asyncio
async def test_get_task_by_id(db_session, user, category):
    repo = TaskRepository(db_session)
    task = await repo.create(
        title="Finish project",
        description="Complete the backend part",
        priority=3,
        due_date=datetime(2023, 12, 31),
        is_completed=False,
        owner_id=user.id,
        category_id=category.id,
    )

    fetched_task = await repo.get_by_id(task_id=task.id)
    assert fetched_task is not None
    assert fetched_task.title == "Finish project"


@pytest.mark.asyncio
async def test_get_tasks_by_owner(db_session, user, category):
    repo = TaskRepository(db_session)
    await repo.create(
        title="Task 1",
        description="Description 1",
        priority=1,
        due_date=datetime(2023, 12, 31),
        is_completed=False,
        owner_id=user.id,
        category_id=category.id,
    )
    await repo.create(
        title="Task 2",
        description="Description 2",
        priority=2,
        due_date=datetime(2023, 12, 31),
        is_completed=False,
        owner_id=1,
        category_id=user.id,
    )

    tasks = await repo.get_by_owner(owner_id=1)
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


@pytest.mark.asyncio
async def test_update_task(db_session, user, category):
    repo = TaskRepository(db_session)
    task = await repo.create(
        title="Finish project",
        description="Complete the backend part",
        priority=3,
        due_date=datetime(2023, 12, 31),
        is_completed=False,
        owner_id=user.id,
        category_id=category.id,
    )

    updated_data = {"title": "Updated Task", "priority": 5}
    updated_task = await repo.update(task_id=task.id, updated_data=updated_data)

    assert updated_task.title == "Updated Task"
    assert updated_task.priority == 5


@pytest.mark.asyncio
async def test_delete_task(db_session, user, category):
    repo = TaskRepository(db_session)
    task = await repo.create(
        title="Finish project",
        description="Complete the backend part",
        priority=3,
        due_date=datetime(2023, 12, 31),
        is_completed=False,
        owner_id=user.id,
        category_id=category.id,
    )

    success = await repo.delete(task_id=task.id)
    assert success is True

    deleted_task = await repo.get_by_id(task_id=task.id)
    assert deleted_task is None
