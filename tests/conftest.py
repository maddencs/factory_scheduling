import asyncio
from unittest.mock import Mock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.api.main import app
from src.database import DATABASE_ASYNC_URL, get_async_session
from src.models.base import Base


@pytest_asyncio.fixture(scope="function")
async def db_session():
    test_engine = create_async_engine(DATABASE_ASYNC_URL, echo=False, future=True)
    TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)

    async with TestSessionLocal() as session:
        yield session

        # Disable FK checks so truncation order doesn't matter
        await session.execute(text("SET session_replication_role = replica;"))

        # Truncate all tables and reset sequences
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;'))

        # Re-enable FK constraints
        await session.execute(text("SET session_replication_role = DEFAULT;"))
        await session.commit()


@pytest_asyncio.fixture(scope="function")
async def test_client(db_session: AsyncSession):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:

        async def override_get_session():
            yield db_session

        app.dependency_overrides[get_async_session] = override_get_session
        yield client


@pytest.fixture(scope="session")
async def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def mock_info(db_session: AsyncSession):
    mock_info = Mock()
    mock_info.context = {"session": db_session}
    yield mock_info
