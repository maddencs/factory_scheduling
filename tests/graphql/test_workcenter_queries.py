from datetime import timedelta

import pytest

from src.models import Part, Workcenter
from tests.factories.workcenter import workcenter_factory


@pytest.mark.asyncio
async def test_workcenter_query_all_parts(db_session, test_client):
    workcenter = await workcenter_factory(name="Workcenter A", session=db_session)

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
