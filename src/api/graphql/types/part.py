import strawberry

from src.models import Part


@strawberry.type
class WorkcenterType:
    id: int
    name: str


@strawberry.type
class PartType:
    id: int
    name: str
    lead_time_seconds: int
    workcenter: WorkcenterType


def map_part_to_type(part: Part) -> PartType:
    return PartType(
        id=part.id,
        name=part.name,
        lead_time_seconds=int(part.lead_time.total_seconds()),
        workcenter=WorkcenterType(
            id=part.workcenter.id,
            name=part.workcenter.name,
        ),
    )
