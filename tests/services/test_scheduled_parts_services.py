from datetime import datetime, timedelta

import pytest

from src.services.scheduled_parts import all_scheduled_parts
from tests.factories.bill_of_materials import bom_factory
from tests.factories.order import order_factory
from tests.factories.part import part_factory
from tests.factories.scheduled_part import scheduled_part_factory
from tests.factories.workcenter import workcenter_factory


@pytest.mark.asyncio
async def test_service_scheduled_part_all_scheduled_parts(db_session):
    workcenter = await workcenter_factory(name="Workcenter A", session=db_session)

    part = await part_factory(
        session=db_session,
        name="Widget A",
        lead_time=timedelta(days=1),
        workcenter_id=workcenter.id,
    )
    bom = await bom_factory(name="Robot", session=db_session)
    order = await order_factory(bill_of_materials_id=bom.id, session=db_session)
    scheduled_part = await scheduled_part_factory(
        session=db_session,
        part_id=part.id,
        order_id=order.id,
        scheduled_start=datetime.now(),
    )

    scheduled_parts = await all_scheduled_parts(db_session)

    assert len(scheduled_parts) == 1
    assert scheduled_parts[0].id == scheduled_part.id
