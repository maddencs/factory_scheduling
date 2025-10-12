from sqlalchemy.ext.asyncio import AsyncSession

from src.models import BillOfMaterials


async def bom_factory(
    session: AsyncSession,
    name: str,
) -> BillOfMaterials:
    bom = BillOfMaterials(
        name=name,
    )
    session.add(bom)
    await session.commit()
    await session.refresh(bom)
    return bom
