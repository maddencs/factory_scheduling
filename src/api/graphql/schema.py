import strawberry

from .schemas.order_mutation import OrderMutation
from .schemas.part_mutation import PartMutation
from .schemas.part_query import PartQuery
from .schemas.scheduled_part_query import ScheduledPartQuery
from .schemas.workcenter_query import WorkcenterQuery


@strawberry.type
class Query(PartQuery, WorkcenterQuery, ScheduledPartQuery):
    pass


@strawberry.type
class Mutation(PartMutation, OrderMutation):
    pass


schema = strawberry.Schema(mutation=Mutation, query=Query)
