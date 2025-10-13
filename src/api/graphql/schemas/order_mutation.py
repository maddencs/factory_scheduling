import strawberry
from strawberry.types import Info

from src.api.graphql.types.order import OrderType, map_order_to_type
from src.services.order import submit_order


@strawberry.type
class OrderMutation:
    @strawberry.mutation
    async def submit_order(
        self,
        info: Info,
        bill_of_materials_id: int,
    ) -> OrderType:
        session = info.context["session"]
        order = await submit_order(
            bill_of_materials_id=bill_of_materials_id,
            session=session,
        )
        await session.refresh(order, ["bill_of_materials"])
        return map_order_to_type(order)
