import pytest

from app.core.security import get_password_hash
from app.users.repository import UserRepository


@pytest.mark.asyncio
async def test_create_user(db_session):
    repo = UserRepository(db_session)
    hashed_password = get_password_hash("password123")
    user = await repo.create(email="test@example.com", hashed_password=hashed_password)

    assert user.email == "test@example.com"
    assert user.hashed_password == hashed_password


@pytest.mark.asyncio
async def test_get_user_by_email(db_session):
    repo = UserRepository(db_session)
    hashed_password = get_password_hash("password123")
    await repo.create(email="test@example.com", hashed_password=hashed_password)

    user = await repo.get_by_email(email="test@example.com")
    assert user is not None
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_update_user(db_session):
    repo = UserRepository(db_session)
    hashed_password = get_password_hash("password123")
    user = await repo.create(email="test@example.com", hashed_password=hashed_password)

    updated_data = {"email": "updated@example.com"}
    updated_user = await repo.update(user_id=user.id, updated_data=updated_data)

    assert updated_user.email == "updated@example.com"
