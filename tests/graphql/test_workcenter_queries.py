import pytest

from tests.factories.workcenter import workcenter_factory


@pytest.mark.asyncio
async def test_workcenter_query_all_workcenters(db_session, test_client):
    workcenter = await workcenter_factory(name="Workcenter A", session=db_session)

    query = """
        query {
            allWorkcenters {
                id
                name
            }
        }
    """
    response = await test_client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["allWorkcenters"][0]["id"] == workcenter.id
