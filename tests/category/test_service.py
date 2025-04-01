from unittest.mock import AsyncMock

import pytest

from app.categories.repository import CategoryRepository
from app.categories.service import CategoryService


@pytest.mark.asyncio
async def test_get_nonexistent_category():
    # Мок репозитория возвращает None (категория не найдена)
    mock_repo = AsyncMock(spec=CategoryRepository)
    mock_repo.get_by_id.return_value = None

    service = CategoryService(repository=mock_repo)

    category = await service.get_category(category_id=999)
    assert category is None


@pytest.mark.asyncio
async def test_update_nonexistent_category():
    # Мок репозитория возвращает None (категория не найдена)
    mock_repo = AsyncMock(spec=CategoryRepository)
    mock_repo.update.return_value = None

    service = CategoryService(repository=mock_repo)

    updated_category = await service.update_category(
        category_id=999, updated_data={"name": "Updated Name"}
    )
    assert updated_category is None


@pytest.mark.asyncio
async def test_delete_nonexistent_category():
    # Мок репозитория возвращает False (категория не найдена)
    mock_repo = AsyncMock(spec=CategoryRepository)
    mock_repo.delete.return_value = False

    service = CategoryService(repository=mock_repo)

    success = await service.delete_category(category_id=999)
    assert success is False
