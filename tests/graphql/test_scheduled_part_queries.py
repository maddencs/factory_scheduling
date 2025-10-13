from datetime import datetime, timedelta

import pytest

from tests.factories.bill_of_materials import bom_factory
from tests.factories.order import order_factory
from tests.factories.part import part_factory
from tests.factories.scheduled_part import scheduled_part_factory
from tests.factories.workcenter import workcenter_factory


@pytest.mark.asyncio
async def test_part_query_all_parts(db_session, test_client):
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

    query = """
        query {
            allScheduledParts {
                id
                order {
                    id
                }
                part {
                    id
                    name
                    workcenter {
                        id
                        name
                    }
                }
            }
        }
    """
    response = await test_client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["allScheduledParts"][0]["id"] == scheduled_part.id
    assert response.json()["data"]["allScheduledParts"][0]["part"]["id"] == part.id
    assert response.json()["data"]["allScheduledParts"][0]["part"]["name"] == part.name
    assert response.json()["data"]["allScheduledParts"][0]["order"]["id"] == order.id
    assert response.json()["data"]["allScheduledParts"][0]["part"]["workcenter"]["id"] == workcenter.id
    assert response.json()["data"]["allScheduledParts"][0]["part"]["workcenter"]["name"] == workcenter.name
