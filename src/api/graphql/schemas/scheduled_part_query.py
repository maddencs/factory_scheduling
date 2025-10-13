from typing import List

import strawberry
from strawberry.types import Info

from src.services.scheduled_parts import all_scheduled_parts
from src.api.graphql.types.scheduled_part import ScheduledPartType, map_scheduled_part_to_type


@strawberry.type
class ScheduledPartQuery:
    @strawberry.field
    async def all_scheduled_parts(self, info: Info) -> List[ScheduledPartType]:
        scheduled_parts = await all_scheduled_parts(info.context["session"])
        return [
            map_scheduled_part_to_type(scheduled_part, info.context["session"]) for scheduled_part in scheduled_parts
        ]
