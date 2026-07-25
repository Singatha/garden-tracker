from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import garden_member
from app.models import GardenMembership, GrowingArea
from app.schemas import AreaCreate, AreaRead

router = APIRouter(prefix="/gardens/{garden_id}/areas", tags=["growing areas"])


@router.get("", response_model=list[AreaRead])
async def list_areas(
    garden_id: int,
    _: GardenMembership = Depends(garden_member),
    db: AsyncSession = Depends(get_db),
) -> list[GrowingArea]:
    return list(
        await db.scalars(
            select(GrowingArea).where(GrowingArea.garden_id == garden_id).order_by(GrowingArea.name)
        )
    )


@router.post("", response_model=AreaRead, status_code=status.HTTP_201_CREATED)
async def create_area(
    garden_id: int,
    payload: AreaCreate,
    _: GardenMembership = Depends(garden_member),
    db: AsyncSession = Depends(get_db),
) -> GrowingArea:
    area = GrowingArea(garden_id=garden_id, **payload.model_dump())
    db.add(area)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409, detail="An area with this name already exists"
        ) from None
    await db.refresh(area)
    return area
