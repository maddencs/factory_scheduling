from datetime import timedelta

import strawberry
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from strawberry.types import Info

from src.models.part import Part


async def all_parts(info: Info):
    session = info.context["session"]
    parts = await session.execute(select(Part).options(selectinload(Part.workcenter)))
    return parts.scalars().all()


async def add_part(
    name: str,
    workcenter_id: int,
    lead_time: timedelta,
    info: Info,
) -> Part:
    session = info.context["session"]
    part = Part(
        name=name,
        lead_time=lead_time,
        workcenter_id=workcenter_id,
    )
    session.add(part)
    await session.commit()
    await session.refresh(part)
    return part
