from typing import List

import strawberry
from strawberry.types import Info

from src.api.graphql.resolvers.workcenter import all_workcenters
from src.api.graphql.types.workcenter import (WorkcenterType,
                                              map_workcenter_to_type)


@strawberry.type
class WorkcenterQuery:
    @strawberry.field
    async def all_workcenters(self, info: Info) -> List[WorkcenterType]:
        workcenters = await all_workcenters(info)
        data = [map_workcenter_to_type(workcenter) for workcenter in workcenters]
        return data
