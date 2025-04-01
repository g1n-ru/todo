from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.schema import RefreshToken, Token, UserChangePassword
from app.core.config import settings
from app.core.dependencies import get_user_service
from app.core.security import create_jwt_token, decode_jwt_token
from app.users.schema import UserCreate, UserOut
from app.users.service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate, service: UserService = Depends(get_user_service)
):
    try:
        return await service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаем access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_jwt_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # Создаем refresh token
    refresh_token_value = create_jwt_token(
        data={"sub": user.email, "type": "refresh"},
        expires_delta=timedelta(settings.refresh_token_expire_minutes),
        secret_key=settings.secret_key,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_value,
        "token_type": "bearer",
    }


@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(
    refresh_token: RefreshToken,
):
    # Проверяем refresh token
    payload = decode_jwt_token(
        refresh_token.refresh_token, secret_key=settings.secret_key
    )
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    # Создаем новые токены
    access_token = create_jwt_token(
        data={"sub": payload["sub"]},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    new_refresh_token = create_jwt_token(
        data={"sub": payload["sub"], "type": "refresh"},
        expires_delta=timedelta(minutes=settings.refresh_token_expire_minutes),
        secret_key=settings.secret_key,
    )

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/change-password", response_model=UserOut, status_code=status.HTTP_200_OK)
async def change_password(
    user_data: UserChangePassword, service: UserService = Depends(get_user_service)
):
    try:
        return await service.change_password(**user_data.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
