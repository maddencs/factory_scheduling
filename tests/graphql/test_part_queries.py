from datetime import timedelta

import pytest

from src.models import Part, Workcenter


@pytest.mark.asyncio
async def test_query_all_parts(db_session, test_client):
    workcenter = Workcenter(name="Workcenter A")
    db_session.add(workcenter)
    await db_session.commit()
    await db_session.refresh(workcenter)

    part = Part(
        name="Widget A",
        workcenter_id=workcenter.id,
        lead_time=timedelta(days=1),
    )
    db_session.add(part)
    await db_session.commit()
    await db_session.refresh(part)

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
