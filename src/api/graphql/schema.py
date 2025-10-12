import strawberry

from .schemas.order_mutation import OrderMutation
from .schemas.part_mutation import PartMutation
from .schemas.part_query import PartQuery
from .schemas.workcenter_query import WorkcenterQuery


@strawberry.type
class Query(PartQuery, WorkcenterQuery):
    pass


@strawberry.type
class Mutation(PartMutation, OrderMutation):
    pass


schema = strawberry.Schema(mutation=Mutation, query=Query)
