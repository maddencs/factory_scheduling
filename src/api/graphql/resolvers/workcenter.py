from sqlalchemy import select
from strawberry.types import Info

from src.models import Workcenter


async def all_workcenters(info: Info):
    session = info.context["session"]
    workcenters = await session.execute(select(Workcenter))
    return workcenters.scalars().all()
