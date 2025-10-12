from datetime import timedelta

import pytest

from src.services.part import all_parts
from tests.factories.part import part_factory
from tests.factories.workcenter import workcenter_factory


@pytest.mark.asyncio
async def test_workcenter_service_all_workcenters(db_session):
    workcenter = await workcenter_factory(name="Workcenter A", session=db_session)

    part = await part_factory(
        session=db_session,
        name="Widget A",
        lead_time=timedelta(days=1),
        workcenter_id=workcenter.id,
    )

    parts = await all_parts(db_session)

    assert len(parts) == 1
    assert parts[0].id == part.id
    assert parts[0].name == part.name
    assert parts[0].lead_time == part.lead_time
    assert parts[0].workcenter.id == workcenter.id
    assert parts[0].workcenter.name == workcenter.name
