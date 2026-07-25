from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import garden_member
from app.models import GardenMembership, GardenTask, Planting, User, utcnow
from app.schemas import TaskCreate, TaskRead
from app.security import current_user

router = APIRouter(prefix="/gardens/{garden_id}/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
async def list_tasks(
    garden_id: int,
    include_completed: bool = False,
    _: GardenMembership = Depends(garden_member),
    db: AsyncSession = Depends(get_db),
) -> list[GardenTask]:
    query = select(GardenTask).where(GardenTask.garden_id == garden_id)
    if not include_completed:
        query = query.where(GardenTask.completed_at.is_(None))
    return list(await db.scalars(query.order_by(GardenTask.due_on, GardenTask.id)))


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    garden_id: int,
    payload: TaskCreate,
    _: GardenMembership = Depends(garden_member),
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> GardenTask:
    if payload.planting_id is not None:
        planting_id = await db.scalar(
            select(Planting.id).where(
                Planting.id == payload.planting_id, Planting.garden_id == garden_id
            )
        )
        if planting_id is None:
            raise HTTPException(status_code=422, detail="Planting does not belong to this garden")
    task = GardenTask(garden_id=garden_id, created_by_id=user.id, **payload.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.post("/{task_id}/complete", response_model=TaskRead)
async def complete_task(
    garden_id: int,
    task_id: int,
    _: GardenMembership = Depends(garden_member),
    db: AsyncSession = Depends(get_db),
) -> GardenTask:
    task = await db.scalar(
        select(GardenTask).where(GardenTask.id == task_id, GardenTask.garden_id == garden_id)
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed_at = utcnow()
    await db.commit()
    await db.refresh(task)
    return task
