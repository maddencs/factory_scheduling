from sqlalchemy.ext.asyncio import AsyncSession

from src.services.order_scheduling import OrderScheduler
from src.models import Order


async def submit_order(
    bill_of_materials_id: int,
    session: AsyncSession,
) -> Order:
    order = Order(
        bill_of_materials_id=bill_of_materials_id,
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)

    await OrderScheduler().schedule(order, session)

    return order
