from fastapi import Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import GardenMembership, User
from app.security import current_user


async def garden_member(
    garden_id: int = Path(),
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> GardenMembership:
    membership = await db.scalar(
        select(GardenMembership).where(
            GardenMembership.garden_id == garden_id,
            GardenMembership.user_id == user.id,
            GardenMembership.active.is_(True),
        )
    )
    if membership is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Garden not found")
    return membership
