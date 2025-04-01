from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import Category


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, name: str, owner_id: int) -> Category:
        category = Category(name=name, owner_id=owner_id)
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def get_by_id(self, category_id: int) -> Category | None:
        result = await self.db.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalars().first()

    async def get_by_owner(self, owner_id: int) -> list[Category]:
        result = await self.db.execute(
            select(Category).where(Category.owner_id == owner_id)
        )
        return result.scalars().all()

    async def update(self, category_id: int, updated_data: dict) -> Category | None:
        result = await self.db.execute(
            select(Category).where(Category.id == category_id)
        )
        category = result.scalars().first()
        if not category:
            return None
        for key, value in updated_data.items():
            setattr(category, key, value)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete(self, category_id: int) -> bool:
        category = await self.get_by_id(category_id)
        if not category:
            return False
        await self.db.delete(category)
        await self.db.commit()
        return True
