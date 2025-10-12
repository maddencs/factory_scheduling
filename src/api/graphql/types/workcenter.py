import strawberry

from src.models import Workcenter


@strawberry.type
class WorkcenterType:
    id: int
    name: str


def map_workcenter_to_type(workcenter: Workcenter) -> WorkcenterType:
    return WorkcenterType(
        id=workcenter.id,
        name=workcenter.name,
    )
