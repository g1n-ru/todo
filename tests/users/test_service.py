from unittest.mock import AsyncMock

import pytest

from app.users.models import User
from app.users.repository import UserRepository
from app.users.schema import UserCreate
from app.users.service import UserService


@pytest.mark.asyncio
async def test_register_user_with_existing_email():
    # Мок репозитория возвращает существующего пользователя
    mock_repo = AsyncMock(spec=UserRepository)
    mock_repo.create.return_value = User(
        **{
            "id": 1,
            "email": "test@example.com",
            "hashed_password": "hash",
            "is_active": True,
        }
    )

    service = UserService(repository=mock_repo)

    await service.register_user(
        UserCreate(email="test@example.com", password="password123")
    )


@pytest.mark.asyncio
async def test_authenticate_user_with_wrong_password():
    # Мок репозитория возвращает пользователя, но пароль неверный
    mock_repo = AsyncMock(spec=UserRepository)
    mock_repo.get_by_email.return_value = User(
        **{
            "id": 1,
            "email": "test@example.com",
            "hashed_password": "$2b$12$Q0DGFUnTiP18ZOdvlp7YeuDH51USHV9ay.fVbYBObLxCKUw3G4JZ.",
        }
    )

    service = UserService(repository=mock_repo)

    user = await service.authenticate_user(
        email="test@example.com", password="wrong_password"
    )
    assert user is None


@pytest.mark.asyncio
async def test_authenticate_user_with_nonexistent_email():
    # Мок репозитория возвращает None (пользователь не найден)
    mock_repo = AsyncMock(spec=UserRepository)
    mock_repo.get_by_email.return_value = None

    service = UserService(repository=mock_repo)

    user = await service.authenticate_user(
        email="nonexistent@example.com", password="password123"
    )
    assert user is None
