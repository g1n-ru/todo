from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Хэширование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Генерация JWT
def create_jwt_token(
    data: dict, expires_delta: timedelta | None = None, secret_key: str = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, secret_key or settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


# Декодирование JWT
def decode_jwt_token(token: str, secret_key: str = None):
    try:
        payload = jwt.decode(
            token, secret_key or settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None


# Хэширование и проверка паролей
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
