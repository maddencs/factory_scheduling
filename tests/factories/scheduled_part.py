from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import ScheduledPart


async def scheduled_part_factory(
    session: AsyncSession,
    part_id: int,
    order_id: int,
    scheduled_start: datetime,
) -> ScheduledPart:
    scheduled_part = ScheduledPart(
        part_id=part_id,
        order_id=order_id,
        scheduled_start=scheduled_start,
    )
    session.add(scheduled_part)
    await session.commit()
    await session.refresh(scheduled_part)
    return scheduled_part
