from fastapi import status
from httpx import AsyncClient


async def test_register_user(client: AsyncClient, db_session):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "newuser@example.com", "password": "password123"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "newuser@example.com"


async def test_login(user, client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_refresh_token(client: AsyncClient, db_session, user):
    # Логин для получения refresh token
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "password123"},
    )
    refresh_token = login_response.json()["refresh_token"]

    # Обновление токена
    response = await client.post(
        "/api/v1/auth/refresh-token", json={"refresh_token": refresh_token}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


async def test_register_existing_user(client: AsyncClient, db_session, user):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "User already exists" in response.json()["detail"]


async def test_login_with_invalid_credentials(client: AsyncClient, db_session):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistent@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect email or password" in response.json()["detail"]


async def test_refresh_with_invalid_token(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/refresh-token", json={"refresh_token": "invalid-token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid refresh token" in response.json()["detail"]


async def test_change_password(client: AsyncClient, db_session, user):
    response = await client.post(
        "/api/v1/auth/change-password",
        json={
            "email": "test@example.com",
            "old_password": "password123",
            "new_password": "password123!",
        },
    )
    assert response.status_code == status.HTTP_200_OK


async def test_change_password_with_wrong_password(
    client: AsyncClient, db_session, user
):
    response = await client.post(
        "/api/v1/auth/change-password",
        json={
            "email": "test@example.com",
            "old_password": "password",
            "new_password": "password123!",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
