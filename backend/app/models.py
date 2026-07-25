from datetime import UTC, date, datetime
from enum import StrEnum

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class MembershipRole(StrEnum):
    owner = "owner"
    helper = "helper"


class AreaType(StrEnum):
    bed = "bed"
    container = "container"
    row = "row"
    greenhouse = "greenhouse"
    other = "other"


class PlantingStatus(StrEnum):
    planned = "planned"
    growing = "growing"
    harvested = "harvested"
    finished = "finished"
    failed = "failed"


class PlantingMethod(StrEnum):
    direct_sown = "direct_sown"
    transplanted = "transplanted"
    existing = "existing"


class EventType(StrEnum):
    watered = "watered"
    fertilized = "fertilized"
    pruned = "pruned"
    transplanted = "transplanted"
    pest_observed = "pest_observed"
    disease_observed = "disease_observed"
    note = "note"
    removed = "removed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class Garden(Base):
    __tablename__ = "gardens"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    memberships: Mapped[list["GardenMembership"]] = relationship(cascade="all, delete-orphan")


class GardenMembership(Base):
    __tablename__ = "garden_memberships"
    __table_args__ = (UniqueConstraint("garden_id", "user_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    garden_id: Mapped[int] = mapped_column(ForeignKey("gardens.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[MembershipRole] = mapped_column(Enum(MembershipRole))
    active: Mapped[bool] = mapped_column(default=True)


class GrowingArea(Base):
    __tablename__ = "growing_areas"
    __table_args__ = (UniqueConstraint("garden_id", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    garden_id: Mapped[int] = mapped_column(ForeignKey("gardens.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    area_type: Mapped[AreaType] = mapped_column(Enum(AreaType), default=AreaType.bed)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class Planting(Base):
    __tablename__ = "plantings"

    id: Mapped[int] = mapped_column(primary_key=True)
    garden_id: Mapped[int] = mapped_column(ForeignKey("gardens.id", ondelete="CASCADE"), index=True)
    growing_area_id: Mapped[int] = mapped_column(
        ForeignKey("growing_areas.id", ondelete="RESTRICT"), index=True
    )
    crop: Mapped[str] = mapped_column(String(120))
    variety: Mapped[str | None] = mapped_column(String(120), nullable=True)
    quantity: Mapped[int] = mapped_column(default=1)
    method: Mapped[PlantingMethod] = mapped_column(Enum(PlantingMethod))
    planted_on: Mapped[date] = mapped_column(Date)
    expected_harvest_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[PlantingStatus] = mapped_column(
        Enum(PlantingStatus), default=PlantingStatus.growing
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class GardenEvent(Base):
    __tablename__ = "garden_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    garden_id: Mapped[int] = mapped_column(ForeignKey("gardens.id", ondelete="CASCADE"), index=True)
    planting_id: Mapped[int] = mapped_column(
        ForeignKey("plantings.id", ondelete="CASCADE"), index=True
    )
    event_type: Mapped[EventType] = mapped_column(Enum(EventType))
    occurred_on: Mapped[date] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))


class GardenTask(Base):
    __tablename__ = "garden_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    garden_id: Mapped[int] = mapped_column(ForeignKey("gardens.id", ondelete="CASCADE"), index=True)
    planting_id: Mapped[int | None] = mapped_column(
        ForeignKey("plantings.id", ondelete="CASCADE"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(160))
    due_on: Mapped[date] = mapped_column(Date, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))


class Harvest(Base):
    __tablename__ = "harvests"

    id: Mapped[int] = mapped_column(primary_key=True)
    garden_id: Mapped[int] = mapped_column(ForeignKey("gardens.id", ondelete="CASCADE"), index=True)
    planting_id: Mapped[int] = mapped_column(
        ForeignKey("plantings.id", ondelete="CASCADE"), index=True
    )
    harvested_on: Mapped[date] = mapped_column(Date)
    quantity: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(30))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
