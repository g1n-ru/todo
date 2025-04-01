from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.categories.repository import CategoryRepository
from app.categories.service import CategoryService
from app.core.db import get_db
from app.tasks.repository import TaskRepository
from app.tasks.service import TaskService
from app.users.repository import UserRepository
from app.users.service import UserService


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_repo = UserRepository(db)
    return UserService(repository=user_repo)


def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    category_repo = CategoryRepository(db)
    return CategoryService(repository=category_repo)


def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    task_repo = TaskRepository(db)
    return TaskService(repository=task_repo)
