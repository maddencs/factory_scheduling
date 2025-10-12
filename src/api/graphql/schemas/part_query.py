from typing import List

import strawberry
from strawberry.types import Info

from src.api.graphql.types.part import PartType, map_part_to_type
from src.services.part import all_parts


@strawberry.type
class PartQuery:
    @strawberry.field
    async def all_parts(self, info: Info) -> List[PartType]:
        parts = await all_parts(info.context["session"])
        data = [map_part_to_type(part) for part in parts]
        return data
