import strawberry

from .schemas.query_schema import PartQuery


@strawberry.type
class Query(PartQuery):
    pass


schema = strawberry.Schema(query=Query)
