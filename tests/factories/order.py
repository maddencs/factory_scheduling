from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Order


async def order_factory(
    session: AsyncSession,
    bill_of_materials_id: int,
) -> Order:
    order = Order(bill_of_materials_id=bill_of_materials_id)
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order
