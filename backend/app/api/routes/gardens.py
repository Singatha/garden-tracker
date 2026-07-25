from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import garden_member
from app.models import Garden, GardenMembership, MembershipRole, User
from app.schemas import GardenCreate, GardenRead
from app.security import current_user

router = APIRouter(prefix="/gardens", tags=["gardens"])


@router.get("", response_model=list[GardenRead])
async def list_gardens(
    user: User = Depends(current_user), db: AsyncSession = Depends(get_db)
) -> list[Garden]:
    result = await db.scalars(
        select(Garden)
        .join(GardenMembership)
        .where(GardenMembership.user_id == user.id, GardenMembership.active.is_(True))
        .order_by(Garden.name)
    )
    return list(result)


@router.post("", response_model=GardenRead, status_code=status.HTTP_201_CREATED)
async def create_garden(
    payload: GardenCreate,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> Garden:
    garden = Garden(name=payload.name.strip(), location=payload.location)
    db.add(garden)
    await db.flush()
    db.add(
        GardenMembership(
            garden_id=garden.id, user_id=user.id, role=MembershipRole.owner, active=True
        )
    )
    await db.commit()
    await db.refresh(garden)
    return garden


@router.get("/{garden_id}", response_model=GardenRead)
async def get_garden(
    garden_id: int,
    _: GardenMembership = Depends(garden_member),
    db: AsyncSession = Depends(get_db),
) -> Garden:
    return await db.get_one(Garden, garden_id)
