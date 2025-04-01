import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_category(auth_client: AsyncClient, db_session, user):
    response = await auth_client.post(
        "/api/v1/categories/", json={"name": "New Category"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Category"


@pytest.mark.asyncio
async def test_get_category(auth_client: AsyncClient, category, db_session, user):
    response = await auth_client.get(
        f"/api/v1/categories/{category.id}",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Test Category"


@pytest.mark.asyncio
async def test_update_category(auth_client: AsyncClient, category, db_session, user):
    response = await auth_client.put(
        f"/api/v1/categories/{category.id}", json={"name": "Updated Category"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Category"


@pytest.mark.asyncio
async def test_delete_category(auth_client: AsyncClient, category, db_session, user):
    response = await auth_client.delete(
        f"/api/v1/categories/{category.id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "Category deleted"


@pytest.mark.asyncio
async def test_get_nonexistent_category(auth_client: AsyncClient, db_session, user):
    response = await auth_client.get(
        "/api/v1/categories/999",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
