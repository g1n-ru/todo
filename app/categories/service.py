from app.categories.repository import CategoryRepository
from app.categories.schema import CategoryCreate, CategoryOut


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def create_category(
        self, category: CategoryCreate, owner_id: int
    ) -> CategoryOut:
        db_category = await self.repository.create(category.name, owner_id)
        return CategoryOut(
            id=db_category.id, name=db_category.name, owner_id=db_category.owner_id
        )

    async def get_category(self, category_id: int) -> CategoryOut | None:
        db_category = await self.repository.get_by_id(category_id)
        if not db_category:
            return None
        return CategoryOut(
            id=db_category.id, name=db_category.name, owner_id=db_category.owner_id
        )

    async def update_category(
        self, category_id: int, updated_data: dict
    ) -> CategoryOut | None:
        db_category = await self.repository.update(category_id, updated_data)
        if not db_category:
            return None
        return CategoryOut(
            id=db_category.id, name=db_category.name, owner_id=db_category.owner_id
        )

    async def delete_category(self, category_id: int) -> bool:
        return await self.repository.delete(category_id)

    async def get_categories_by_owner(
        self,
        owner_id: int,
    ) -> list[CategoryOut]:
        db_tasks = await self.repository.get_by_owner(owner_id)
        return [CategoryOut.model_validate(t, from_attributes=True) for t in db_tasks]
