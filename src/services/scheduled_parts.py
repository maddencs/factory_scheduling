from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import ScheduledPart


async def all_scheduled_parts(session: AsyncSession):
    scheduled_parts = await session.execute(
        select(ScheduledPart)
        .options(selectinload(ScheduledPart.part))
        .options(selectinload(ScheduledPart.order))
        .order_by(ScheduledPart.scheduled_start.asc())
    )
    return scheduled_parts.scalars().all()
