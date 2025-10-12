from datetime import timedelta

import strawberry
from strawberry.types import Info

from src.api.graphql.types.part import PartType, map_part_to_type
from src.services.part import add_part


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
            lead_time=timedelta(seconds=lead_time_seconds),
            session=info.context["session"],
        )
        return map_part_to_type(part)
