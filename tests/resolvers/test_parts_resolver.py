from datetime import timedelta
from unittest.mock import Mock

import pytest
from sqlalchemy import insert

from src.api.graphql.resolvers.part import get_parts
from src.models import Part, Workcenter


@pytest.mark.asyncio
async def test_get_parts(db_session):
    workcenter = Workcenter(name="Workcenter A")
    db_session.add(workcenter)
    await db_session.commit()
    await db_session.refresh(workcenter)

    part = Part(
        name="Widget A",
        lead_time=timedelta(days=1),
        workcenter_id=workcenter.id,
    )
    db_session.add(part)
    await db_session.commit()
    await db_session.refresh(part)

    mock_info = Mock()
    mock_info.context = {"session": db_session}

    parts = await get_parts(mock_info)

    assert len(parts) == 1
    assert parts[0].id == part.id
    assert parts[0].name == part.name
    assert parts[0].lead_time == part.lead_time
    assert parts[0].workcenter.id == workcenter.id
    assert parts[0].workcenter.name == workcenter.name
