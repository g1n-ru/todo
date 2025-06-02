from typing import Optional

from app.tasks.constants import TaskOrderBy
from app.tasks.repository import TaskRepository
from app.tasks.schema import TaskCreate, TaskOut


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(self, task: TaskCreate, owner_id: int) -> TaskOut:
        db_task = await self.repository.create(
            title=task.title,
            description=task.description,
            priority=task.priority,
            due_date=task.due_date,
            is_completed=task.is_completed,
            owner_id=owner_id,
            category_id=task.category_id,
        )
        return TaskOut.model_validate(db_task, from_attributes=True)

    async def get_task(self, task_id: int) -> TaskOut | None:
        db_task = await self.repository.get_by_id(task_id)
        if not db_task:
            return None
        return TaskOut.model_validate(db_task, from_attributes=True)

    async def get_tasks_by_owner(
        self,
        owner_id: int,
        order_by: TaskOrderBy = TaskOrderBy.DUE_DATE,
        is_completed: bool | None = None,
        category_id: int | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[TaskOut]:
        db_tasks = await self.repository.get_by_owner(
            owner_id, order_by, is_completed, category_id, skip, limit
        )
        return [TaskOut.model_validate(t, from_attributes=True) for t in db_tasks]

    async def update_task(self, task_id: int, updated_data: dict) -> TaskOut | None:
        db_task = await self.repository.update(task_id, updated_data)
        if not db_task:
            return None
        return TaskOut.model_validate(db_task, from_attributes=True)

    async def delete_task(self, task_id: int) -> bool:
        return await self.repository.delete(task_id)

    async def toggle_task_completed(
        self, task_id: int, owner_id: int
    ) -> Optional[TaskOut]:
        """
        Переключает статус завершения задачи (is_completed).
        """
        db_task = await self.repository.get_by_id(task_id)
        if not db_task or db_task.owner_id != owner_id:
            return None

        # Переключаем статус
        updated_data = {"is_completed": not db_task.is_completed}
        db_task = await self.repository.update(task_id, updated_data)

        return TaskOut.model_validate(db_task, from_attributes=True)
