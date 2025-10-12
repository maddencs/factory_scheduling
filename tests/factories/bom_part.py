from sqlalchemy.ext.asyncio import AsyncSession

from src.models import BOMParts


async def bom_part_factory(
    session: AsyncSession,
    bill_of_materials_id: int,
    part_id: int,
    quantity: int,
) -> BOMParts:
    bom_part = BOMParts(bill_of_materials_id=bill_of_materials_id, part_id=part_id, quantity=quantity)
    session.add(bom_part)
    await session.commit()
    await session.refresh(bom_part)
    return bom_part
