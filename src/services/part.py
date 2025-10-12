from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.part import Part


async def all_parts(session: AsyncSession):
    parts = await session.execute(select(Part).options(selectinload(Part.workcenter)))
    return parts.scalars().all()


async def add_part(
    name: str,
    workcenter_id: int,
    lead_time: timedelta,
    session: AsyncSession,
) -> Part:
    part = Part(
        name=name,
        lead_time=lead_time,
        workcenter_id=workcenter_id,
    )
    session.add(part)
    await session.commit()
    await session.refresh(part)

    part = await session.execute(select(Part).options(selectinload(Part.workcenter)).where(Part.id == part.id))
    return part.scalar_one()
