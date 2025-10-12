import strawberry

from .schemas.part_mutation import PartMutation
from .schemas.part_query import PartQuery


@strawberry.type
class Query(PartQuery):
    pass

@strawberry.type
class Mutation(PartMutation):
    pass


schema = strawberry.Schema(mutation=Mutation, query=Query)
