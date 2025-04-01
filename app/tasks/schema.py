from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.categories.schema import CategoryOut
from app.users.schema import UserOut


# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = Field(ge=1, le=5, default=1)
    due_date: Optional[datetime] = None
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(TaskBase):
    category_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None
    category_id: Optional[int] = None


class TaskOut(TaskBase):
    id: int
    owner_id: int
    owner: UserOut
    category: Optional[CategoryOut] = None
