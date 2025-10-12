from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Workcenter


async def all_workcenters(session: AsyncSession):
    workcenters = await session.execute(select(Workcenter))
    return workcenters.scalars().all()
