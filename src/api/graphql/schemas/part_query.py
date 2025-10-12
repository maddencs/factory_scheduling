from typing import List

import strawberry
from strawberry.types import Info

from src.api.graphql.resolvers.part import get_parts
from src.api.graphql.types.part import PartType, map_part_to_type


@strawberry.type
class PartQuery:
    @strawberry.field
    async def all_parts(self, info: Info) -> List[PartType]:
        parts = await get_parts(info)
        data = list()
        for part in parts:
            data.append(map_part_to_type(part))
        return data
