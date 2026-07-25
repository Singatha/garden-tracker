from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import garden_member
from app.models import GardenMembership, GardenTask, Planting, PlantingStatus
from app.schemas import DashboardRead

router = APIRouter(prefix="/gardens/{garden_id}/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardRead)
async def dashboard(
    garden_id: int,
    _: GardenMembership = Depends(garden_member),
    db: AsyncSession = Depends(get_db),
) -> DashboardRead:
    today = date.today()
    active = await db.scalar(
        select(func.count(Planting.id)).where(
            Planting.garden_id == garden_id, Planting.status == PlantingStatus.growing
        )
    )
    open_tasks = list(
        await db.scalars(
            select(GardenTask)
            .where(GardenTask.garden_id == garden_id, GardenTask.completed_at.is_(None))
            .order_by(GardenTask.due_on)
        )
    )
    upcoming = list(
        await db.scalars(
            select(Planting)
            .where(
                Planting.garden_id == garden_id,
                Planting.status == PlantingStatus.growing,
                Planting.expected_harvest_on.between(today, today + timedelta(days=14)),
            )
            .order_by(Planting.expected_harvest_on)
        )
    )
    return DashboardRead(
        active_plantings=active or 0,
        overdue_tasks=[task for task in open_tasks if task.due_on < today],
        due_today=[task for task in open_tasks if task.due_on == today],
        upcoming_harvests=upcoming,
    )
