import pytest

from tests.factories.bill_of_materials import bom_factory


@pytest.mark.asyncio
async def test_order_mutation_submit_order(db_session, test_client):
    bom = await bom_factory(
        session=db_session,
        name="Widget A",
    )

    mutation = f"""
        mutation {{
            submitOrder(
                billOfMaterialsId: {bom.id}
            ) {{
                id
                billOfMaterials {{
                    id
                }}
            }}
        }}
    """
    response = await test_client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200

    created_order = response.json()["data"]["submitOrder"]
    assert created_order["id"] is not None
    assert created_order["billOfMaterials"]["id"] == bom.id
