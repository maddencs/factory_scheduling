from typing import List

import strawberry
from strawberry.types import Info

from src.api.graphql.types.scheduled_part import (ScheduledPartType,
                                                  map_scheduled_part_to_type)
from src.services.scheduled_parts import all_scheduled_parts


@strawberry.type
class ScheduledPartQuery:
    @strawberry.field
    async def all_scheduled_parts(self, info: Info) -> List[ScheduledPartType]:
        session = info.context["session"]
        scheduled_parts = await all_scheduled_parts(session)
        for scheduled_part in scheduled_parts:
            await session.refresh(scheduled_part, ["part"])
            await session.refresh(scheduled_part.part, ["workcenter"])
            await session.refresh(scheduled_part.order, ["bill_of_materials"])
        return [map_scheduled_part_to_type(scheduled_part) for scheduled_part in scheduled_parts]
