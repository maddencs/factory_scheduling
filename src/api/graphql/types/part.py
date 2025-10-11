import strawberry


@strawberry.type
class WorkcenterType:
    id: int
    name: str


@strawberry.type
class PartType:
    id: int
    name: str
    workcenter: WorkcenterType
