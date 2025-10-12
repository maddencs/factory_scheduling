from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Workcenter


async def workcenter_factory(
    session: AsyncSession,
    name: str,
) -> Workcenter:
    workcenter = Workcenter(
        name=name,
    )
    session.add(workcenter)
    await session.commit()
    await session.refresh(workcenter)
    return workcenter
