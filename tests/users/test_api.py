import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_current_user_profile(auth_client: AsyncClient, user):
    response = await auth_client.get("/api/v1/users/me")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == user.email
    assert data["is_active"] is True
