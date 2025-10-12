import pytest

from src.services.order import submit_order
from tests.factories.bill_of_materials import bom_factory
from tests.factories.workcenter import workcenter_factory


@pytest.mark.asyncio
async def test_order_service_submit_order(db_session):
    workcenter = await workcenter_factory(name="Workcenter A", session=db_session)
    bom = await bom_factory(
        session=db_session,
        name="Widget A",
    )

    order = await submit_order(
        bill_of_materials_id=bom.id,
        session=db_session,
    )

    assert order.id is not None
    assert order.bill_of_materials_id == bom.id
