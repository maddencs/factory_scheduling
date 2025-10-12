import strawberry

from .schemas.part_query import PartQuery


@strawberry.type
class Query(PartQuery):
    pass


schema = strawberry.Schema(query=Query)
