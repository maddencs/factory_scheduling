import strawberry

from api.graphql.schemas.part_query import PartQuery


@strawberry.type
class Query(PartQuery):
    pass


schema = strawberry.Schema(query=Query)
