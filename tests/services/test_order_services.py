import pytest

from src.services.order import submit_order
from tests.factories.bill_of_materials import bom_factory


@pytest.mark.asyncio
async def test_order_service_submit_order(db_session):
    bom = await bom_factory(
        session=db_session,
        name="Robot",
    )

    order = await submit_order(
        bill_of_materials_id=bom.id,
        session=db_session,
    )

    assert order.id is not None
    assert order.bill_of_materials_id == bom.id
