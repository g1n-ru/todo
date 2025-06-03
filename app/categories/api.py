from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.categories.schema import CategoryCreate, CategoryOut, CategoryUpdate
from app.categories.service import CategoryService
from app.core.dependencies import get_category_service
from app.users.schema import UserOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    current_user: UserOut = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
):
    return await service.create_category(category_data, owner_id=current_user.id)


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(
    category_id: int,
    current_user: dict = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
):
    category = await service.get_category(category_id)
    if not category or category.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int,
    updated_data: CategoryUpdate,
    current_user: dict = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
):
    category = await service.update_category(
        category_id, updated_data.model_dump(exclude_unset=True)
    )
    if not category or category.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    current_user: dict = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
):
    success = await service.delete_category(category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return {"detail": "Category deleted"}


@router.get("/", response_model=list[CategoryOut])
async def get_tasks(
    current_user: UserOut = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
):
    return await service.get_categories_by_owner(owner_id=current_user.id)
