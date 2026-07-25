from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import garden_member
from app.models import GardenMembership, Harvest, Planting
from app.schemas import HarvestCreate, HarvestRead

router = APIRouter(prefix="/gardens/{garden_id}/harvests", tags=["harvests"])


@router.get("", response_model=list[HarvestRead])
async def list_harvests(
    garden_id: int,
    _: GardenMembership = Depends(garden_member),
    db: AsyncSession = Depends(get_db),
) -> list[Harvest]:
    return list(
        await db.scalars(
            select(Harvest)
            .where(Harvest.garden_id == garden_id)
            .order_by(Harvest.harvested_on.desc(), Harvest.id.desc())
        )
    )


@router.post("", response_model=HarvestRead, status_code=status.HTTP_201_CREATED)
async def create_harvest(
    garden_id: int,
    payload: HarvestCreate,
    _: GardenMembership = Depends(garden_member),
    db: AsyncSession = Depends(get_db),
) -> Harvest:
    planting = await db.scalar(
        select(Planting.id).where(
            Planting.id == payload.planting_id, Planting.garden_id == garden_id
        )
    )
    if planting is None:
        raise HTTPException(status_code=422, detail="Planting does not belong to this garden")
    harvest = Harvest(garden_id=garden_id, **payload.model_dump())
    db.add(harvest)
    await db.commit()
    await db.refresh(harvest)
    return harvest
