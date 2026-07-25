from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import garden_member
from app.models import GardenMembership, GrowingArea, Planting, PlantingStatus
from app.schemas import PlantingCreate, PlantingRead, PlantingUpdate

router = APIRouter(prefix="/gardens/{garden_id}/plantings", tags=["plantings"])


async def checked_area(db: AsyncSession, garden_id: int, area_id: int) -> GrowingArea:
    area = await db.scalar(
        select(GrowingArea).where(GrowingArea.id == area_id, GrowingArea.garden_id == garden_id)
    )
    if area is None:
        raise HTTPException(status_code=422, detail="Growing area does not belong to this garden")
    return area


@router.get("", response_model=list[PlantingRead])
async def list_plantings(
    garden_id: int,
    planting_status: PlantingStatus | None = Query(default=None, alias="status"),
    _: GardenMembership = Depends(garden_member),
    db: AsyncSession = Depends(get_db),
) -> list[Planting]:
    query = select(Planting).where(Planting.garden_id == garden_id)
    if planting_status:
        query = query.where(Planting.status == planting_status)
    return list(await db.scalars(query.order_by(Planting.planted_on.desc(), Planting.crop)))


@router.post("", response_model=PlantingRead, status_code=status.HTTP_201_CREATED)
async def create_planting(
    garden_id: int,
    payload: PlantingCreate,
    _: GardenMembership = Depends(garden_member),
    db: AsyncSession = Depends(get_db),
) -> Planting:
    await checked_area(db, garden_id, payload.growing_area_id)
    planting = Planting(garden_id=garden_id, **payload.model_dump())
    db.add(planting)
    await db.commit()
    await db.refresh(planting)
    return planting


@router.patch("/{planting_id}", response_model=PlantingRead)
async def update_planting(
    garden_id: int,
    planting_id: int,
    payload: PlantingUpdate,
    _: GardenMembership = Depends(garden_member),
    db: AsyncSession = Depends(get_db),
) -> Planting:
    planting = await db.scalar(
        select(Planting).where(Planting.id == planting_id, Planting.garden_id == garden_id)
    )
    if planting is None:
        raise HTTPException(status_code=404, detail="Planting not found")
    planting.status = payload.status
    await db.commit()
    await db.refresh(planting)
    return planting
