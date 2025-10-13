import strawberry

from src.api.graphql.types.bill_of_materials import BillOfMaterialsType
from src.models import Order


@strawberry.type
class OrderType:
    id: int
    bill_of_materials: BillOfMaterialsType


def map_order_to_type(order: Order) -> OrderType:
    return OrderType(
        id=order.id,
        bill_of_materials=BillOfMaterialsType(
            id=order.bill_of_materials.id,
            name=order.bill_of_materials.name,
        ),
    )
