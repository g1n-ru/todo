from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.core.dependencies import get_task_service
from app.tasks.constants import TaskOrderBy
from app.tasks.schema import TaskCreate, TaskOut, TaskUpdate
from app.tasks.service import TaskService
from app.users.schema import UserOut

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: UserOut = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    return await service.create_task(task_data, owner_id=current_user.id)


@router.get("/", response_model=list[TaskOut])
async def get_tasks(
    skip: int = 0,
    limit: int = 10,
    order_by: TaskOrderBy = TaskOrderBy.DUE_DATE,
    is_completed: bool | None = None,
    category_id: int | None = None,
    current_user: UserOut = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    return await service.get_tasks_by_owner(
        owner_id=current_user.id,
        is_completed=is_completed,
        category_id=category_id,
        order_by=order_by,
        skip=skip,
        limit=limit,
    )


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: int,
    current_user: UserOut = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    task = await service.get_task(task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    updated_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    task = await service.update_task(
        task_id, updated_data.model_dump(exclude_unset=True)
    )
    if not task or task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: UserOut = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    success = await service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return {"detail": "Task deleted"}


@router.post("/{task_id}/toggle-completed", response_model=TaskOut)
async def toggle_task_completed(
    task_id: int,
    current_user: UserOut = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """
    Переключает статус завершения задачи (is_completed).
    """
    task = await service.toggle_task_completed(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task
