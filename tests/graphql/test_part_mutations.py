import pytest

from tests.factories.workcenter import workcenter_factory


@pytest.mark.asyncio
async def test_part_mutation_add_part(db_session, test_client):
    workcenter = await workcenter_factory(name="Workcenter A", session=db_session)

    part_name = "Left Robot Arm"
    lead_time_seconds = 120
    mutation = f"""
        mutation {{
            addPart(
            leadTimeSeconds: {lead_time_seconds},
            name: "{part_name}",
            workcenterId: {workcenter.id}
            ) {{
                id
                name
                leadTimeSeconds
                workcenter {{
                        id
                        name
                    }}
                }}
            }}
    """
    response = await test_client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200

    added_part = response.json()["data"]["addPart"]
    assert added_part["id"] is not None
    assert added_part["name"] == part_name
    assert added_part["leadTimeSeconds"] == lead_time_seconds
    assert added_part["workcenter"]["id"] == workcenter.id
    assert added_part["workcenter"]["name"] == workcenter.name
