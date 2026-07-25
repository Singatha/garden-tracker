from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import AreaType, EventType, PlantingMethod, PlantingStatus


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserRead(ORMModel):
    id: int
    email: EmailStr
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class GardenCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    location: str | None = Field(default=None, max_length=200)


class GardenRead(ORMModel):
    id: int
    name: str
    location: str | None


class AreaCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    area_type: AreaType = AreaType.bed
    notes: str | None = None


class AreaRead(ORMModel):
    id: int
    garden_id: int
    name: str
    area_type: AreaType
    notes: str | None


class PlantingCreate(BaseModel):
    growing_area_id: int
    crop: str = Field(min_length=1, max_length=120)
    variety: str | None = Field(default=None, max_length=120)
    quantity: int = Field(default=1, ge=1)
    method: PlantingMethod
    planted_on: date
    expected_harvest_on: date | None = None
    status: PlantingStatus = PlantingStatus.growing
    notes: str | None = None


class PlantingUpdate(BaseModel):
    status: PlantingStatus


class PlantingRead(ORMModel):
    id: int
    garden_id: int
    growing_area_id: int
    crop: str
    variety: str | None
    quantity: int
    method: PlantingMethod
    planted_on: date
    expected_harvest_on: date | None
    status: PlantingStatus
    notes: str | None


class EventCreate(BaseModel):
    planting_id: int
    event_type: EventType
    occurred_on: date
    notes: str | None = None


class EventRead(ORMModel):
    id: int
    planting_id: int
    event_type: EventType
    occurred_on: date
    notes: str | None


class TaskCreate(BaseModel):
    planting_id: int | None = None
    title: str = Field(min_length=1, max_length=160)
    due_on: date
    notes: str | None = None


class TaskRead(ORMModel):
    id: int
    garden_id: int
    planting_id: int | None
    title: str
    due_on: date
    completed_at: datetime | None
    notes: str | None


class HarvestCreate(BaseModel):
    planting_id: int
    harvested_on: date
    quantity: float = Field(gt=0)
    unit: str = Field(min_length=1, max_length=30)
    notes: str | None = None


class HarvestRead(ORMModel):
    id: int
    planting_id: int
    harvested_on: date
    quantity: float
    unit: str
    notes: str | None


class DashboardRead(BaseModel):
    active_plantings: int
    overdue_tasks: list[TaskRead]
    due_today: list[TaskRead]
    upcoming_harvests: list[PlantingRead]
