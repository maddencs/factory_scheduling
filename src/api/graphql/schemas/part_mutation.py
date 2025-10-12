from datetime import timedelta

import strawberry
from strawberry.types import Info

from src.api.graphql.resolvers.part import add_part
from src.api.graphql.types.part import PartType, map_part_to_type


@strawberry.type
class PartMutation:
    @strawberry.mutation
    async def add_part(
        self,
        info: Info,
        name: str,
        lead_time_seconds: int,
        workcenter_id: int,
    ) -> PartType:
        part = await add_part(
            name=name,
            workcenter_id=workcenter_id,
            info=info,
            lead_time=timedelta(seconds=lead_time_seconds),
        )
        return map_part_to_type(part)
