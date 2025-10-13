from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Order
from src.services.order_scheduling import OrderScheduleRunner


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

    await OrderScheduleRunner(session).run(order)

    return order
