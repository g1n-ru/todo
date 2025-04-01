from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# User schemas
class UserBase(BaseModel):
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserOut(UserBase):
    id: int
    is_active: bool
