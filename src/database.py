import os
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PATH = f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DATABASE_ASYNC_URL = f"postgresql+asyncpg://{DB_PATH}"  # For FastAPI
DATABASE_SYNC_URL = f"postgresql://{DB_PATH}"  # For Alembic


engine = create_async_engine(DATABASE_ASYNC_URL, echo=False)
AsyncSession = async_sessionmaker(engine, autoflush=False, autocommit=False, future=True)


@asynccontextmanager
async def get_async_session():
    async with AsyncSession() as session:
        yield session
