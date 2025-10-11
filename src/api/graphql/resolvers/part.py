from sqlalchemy import select
from sqlalchemy.orm import selectinload
from strawberry.types import Info

from src.models.part import Part


async def get_parts(info: Info):
    session = info.context["session"]
    parts = await session.execute(select(Part).options(selectinload(Part.workcenter)))
    return parts.scalars().all()
