import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test-garden.db"
os.environ["SECRET_KEY"] = "test-secret-that-is-longer-than-thirty-two-bytes"

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.database import Base, engine
from app.main import app


@pytest_asyncio.fixture(autouse=True)
async def reset_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as api:
        yield api


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient) -> dict[str, str]:
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "gardener@example.com", "name": "Gardener", "password": "secret123"},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
