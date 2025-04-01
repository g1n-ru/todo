from app.core.security import get_password_hash, verify_password
from app.users.repository import UserRepository
from app.users.schema import UserCreate, UserOut


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_email(self, email: str):
        user = await self.repository.get_by_email(email)
        if not user:
            raise ValueError("User not found")
        return UserOut.model_validate(user, from_attributes=True)

    async def register_user(self, user: UserCreate) -> UserOut:
        hashed_password = get_password_hash(user.password)
        try:
            db_user = await self.repository.create(user.email, hashed_password)
        except Exception:
            raise ValueError("User already exists")
        return UserOut.model_validate(db_user, from_attributes=True)

    async def authenticate_user(self, email: str, password: str) -> UserOut | None:
        user = await self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return UserOut.model_validate(user, from_attributes=True)

    async def update_user(self, user_id: int, updated_data: dict) -> UserOut | None:
        db_user = await self.repository.update(user_id, updated_data)
        if not db_user:
            return None
        return UserOut.model_validate(db_user, from_attributes=True)

    async def change_password(self, email: str, old_password: str, new_password: str):
        user = await self.authenticate_user(email, old_password)
        if not user:
            raise ValueError("Invalid password")

        return await self.update_user(user.id, {"hashed_password": new_password})
