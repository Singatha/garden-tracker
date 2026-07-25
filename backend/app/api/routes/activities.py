from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import garden_member
from app.models import GardenEvent, GardenMembership, Planting, User
from app.schemas import EventCreate, EventRead
from app.security import current_user

router = APIRouter(prefix="/gardens/{garden_id}/activities", tags=["activities"])


@router.get("", response_model=list[EventRead])
async def list_activities(
    garden_id: int,
    _: GardenMembership = Depends(garden_member),
    db: AsyncSession = Depends(get_db),
) -> list[GardenEvent]:
    return list(
        await db.scalars(
            select(GardenEvent)
            .where(GardenEvent.garden_id == garden_id)
            .order_by(GardenEvent.occurred_on.desc(), GardenEvent.id.desc())
            .limit(100)
        )
    )


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_activity(
    garden_id: int,
    payload: EventCreate,
    _: GardenMembership = Depends(garden_member),
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> GardenEvent:
    planting = await db.scalar(
        select(Planting.id).where(
            Planting.id == payload.planting_id, Planting.garden_id == garden_id
        )
    )
    if planting is None:
        raise HTTPException(status_code=422, detail="Planting does not belong to this garden")
    event = GardenEvent(garden_id=garden_id, created_by_id=user.id, **payload.model_dump())
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event
