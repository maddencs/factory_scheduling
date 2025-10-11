import pytest
from httpx import AsyncClient

from src.api.main import app
from src.database import AsyncSession


@pytest.fixture
async def test_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def db_session():
    async with AsyncSession() as session:
        yield session
