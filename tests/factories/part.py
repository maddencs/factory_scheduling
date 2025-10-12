from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Part


async def part_factory(
    session: AsyncSession,
    name: str,
    lead_time: timedelta,
    workcenter_id: int,
) -> Part:
    part = Part(
        name=name,
        lead_time=lead_time,
        workcenter_id=workcenter_id,
    )
    session.add(part)
    await session.commit()
    await session.refresh(part)
    return part
