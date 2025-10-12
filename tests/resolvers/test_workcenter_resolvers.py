from datetime import timedelta

import pytest

from src.api.graphql.resolvers.part import add_part, all_parts
from tests.factories.part import part_factory
from tests.factories.workcenter import workcenter_factory


@pytest.mark.asyncio
async def test_part_resolver_all_workcenters(db_session, mock_info):
    workcenter = await workcenter_factory(name="Workcenter A", session=db_session)

    part = await part_factory(
        session=db_session,
        name="Widget A",
        lead_time=timedelta(days=1),
        workcenter_id=workcenter.id,
    )

    parts = await all_parts(mock_info)

    assert len(parts) == 1
    assert parts[0].id == part.id
    assert parts[0].name == part.name
    assert parts[0].lead_time == part.lead_time
    assert parts[0].workcenter.id == workcenter.id
    assert parts[0].workcenter.name == workcenter.name


@pytest.mark.asyncio
async def test_resolver_add_part(db_session, mock_info):
    workcenter = await workcenter_factory(name="Workcenter A", session=db_session)

    part = await add_part(
        name="Widget A",
        workcenter_id=workcenter.id,
        info=mock_info,
        lead_time=timedelta(days=1),
    )

    assert part.id is not None
