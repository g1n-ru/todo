import pytest

from app.categories.repository import CategoryRepository


@pytest.mark.asyncio
async def test_create_category(db_session, user):
    repo = CategoryRepository(db_session)
    category = await repo.create(name="Work", owner_id=user.id)

    assert category.name == "Work"
    assert category.owner_id == 1


@pytest.mark.asyncio
async def test_get_category_by_id(db_session, user):
    repo = CategoryRepository(db_session)
    category = await repo.create(name="Work", owner_id=user.id)

    fetched_category = await repo.get_by_id(category_id=category.id)
    assert fetched_category is not None
    assert fetched_category.name == "Work"


@pytest.mark.asyncio
async def test_get_categories_by_owner(db_session, user):
    repo = CategoryRepository(db_session)
    await repo.create(name="Work", owner_id=user.id)
    await repo.create(name="Personal", owner_id=user.id)

    categories = await repo.get_by_owner(owner_id=user.id)
    assert len(categories) == 2
    assert categories[0].name == "Work"
    assert categories[1].name == "Personal"


@pytest.mark.asyncio
async def test_update_category(db_session, user):
    repo = CategoryRepository(db_session)
    category = await repo.create(name="Work", owner_id=user.id)

    updated_data = {"name": "Updated Work"}
    updated_category = await repo.update(
        category_id=category.id, updated_data=updated_data
    )

    assert updated_category.name == "Updated Work"


@pytest.mark.asyncio
async def test_delete_category(db_session, user):
    repo = CategoryRepository(db_session)
    category = await repo.create(name="Work", owner_id=user.id)

    success = await repo.delete(category_id=category.id)
    assert success is True

    deleted_category = await repo.get_by_id(category_id=category.id)
    assert deleted_category is None
