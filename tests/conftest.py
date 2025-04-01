from datetime import timedelta

import httpx
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.categories.models import Category
from app.core.app import create_app
from app.core.config import settings
from app.core.db import Base, get_db
from app.core.security import create_jwt_token, get_password_hash
from app.tasks.models import Task
from app.users.models import User


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_app()


@pytest.fixture(scope="function")
async def engine():
    engine = create_async_engine(settings.database_url)

    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Очищаем таблицы после теста
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session(engine, app):
    # Создаем сессию
    async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with engine.connect() as conn:
        async with conn.begin() as tx:
            async with async_session(bind=conn) as session:
                app.dependency_overrides[get_db] = lambda: session
                yield session
        await tx.rollback()


@pytest.fixture(scope="function")
async def user(db_session):
    user = User(
        email="test@example.com", hashed_password=get_password_hash("password123")
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def category(db_session, user):
    category = Category(name="Test Category", owner_id=user.id)
    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)
    return category


@pytest.fixture(scope="function")
async def task(db_session, category, user):
    task = Task(
        title="Test Task",
        category_id=category.id,
        description="Test description",
        priority=1,
        owner_id=user.id,
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    return task


@pytest.fixture
async def client(app: FastAPI):
    async with AsyncClient(
        transport=httpx.ASGITransport(app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def auth_client(app: FastAPI, user):
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_jwt_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    async with AsyncClient(
        transport=httpx.ASGITransport(app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {access_token}"},
    ) as ac:
        yield ac
