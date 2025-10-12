from datetime import timedelta

import pytest

from tests.factories.part import part_factory
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

    query = """
        query {
            allParts {
                id
                name
                workcenter {
                    id
                    name
                }
            }
        }
    """
    response = await test_client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["allParts"][0]["id"] == part.id
