from typing import List

import strawberry
from strawberry.types import Info

from src.api.graphql.resolvers.part import get_parts
from src.api.graphql.types.part import PartType, WorkcenterType


@strawberry.type
class PartQuery:
    @strawberry.field
    async def all_parts(self, info: Info) -> List[PartType]:
        parts = await get_parts(info)
        data = list()
        for part in parts:
            data.append(
                PartType(
                    id=part.id,
                    name=part.name,
                    workcenter=WorkcenterType(
                        id=part.workcenter_id,
                        name=part.workcenter.name,
                    ),
                ),
            )
        return data
