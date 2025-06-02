from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.tasks.constants import TaskOrderBy
from app.users.models import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        title: str,
        description: str,
        priority: int,
        due_date,
        is_completed: bool,
        owner_id: int,
        category_id: int,
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            is_completed=is_completed,
            owner_id=owner_id,
            category_id=category_id,
        )
        self.db.add(task)
        await self.db.commit()
        task = await self.get_by_id(task.id)
        return task

    async def get_by_id(self, task_id: int) -> Task | None:
        result = await self.db.execute(select(Task).where(Task.id == task_id).options(joinedload(Task.owner), selectinload(Task.category)))
        return result.scalars().first()

    async def get_by_owner(
        self,
        owner_id: int,
        order_by: TaskOrderBy = TaskOrderBy.DUE_DATE,
        is_completed: bool | None = None,
        category_id: int | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Task]:
        order = {
            TaskOrderBy.DUE_DATE: Task.due_date.desc(),
            TaskOrderBy.PRIORITY: Task.priority.desc(),
        }
        query = (
            select(Task)
            .where(Task.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .order_by(order[order_by])
            .options(joinedload(Task.owner), selectinload(Task.category))
        )
        if is_completed is not None:
            query = query.where(Task.is_completed == is_completed)
        if category_id is not None:
            query = query.where(Task.category_id == category_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, task_id: int, updated_data: dict) -> Task | None:
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            return None
        for key, value in updated_data.items():
            setattr(task, key, value)
        await self.db.commit()
        task = await self.get_by_id(task_id)
        return task

    async def delete(self, task_id: int) -> bool:
        task = await self.get_by_id(task_id)
        if not task:
            return False
        await self.db.delete(task)
        await self.db.commit()
        return True
