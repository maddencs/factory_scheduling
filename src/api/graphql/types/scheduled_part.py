from datetime import datetime

import strawberry
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.graphql.types.bill_of_materials import BillOfMaterialsType
from src.api.graphql.types.order import OrderType
from src.api.graphql.types.part import PartType
from src.api.graphql.types.workcenter import WorkcenterType
from src.models import ScheduledPart


@strawberry.type
class ScheduledPartType:
    id: int
    name: str
    part: PartType
    lead_time_seconds: int
    part: PartType
    order: OrderType
    scheduled_start: datetime


def map_scheduled_part_to_type(scheduled_part: ScheduledPart, session: AsyncSession) -> ScheduledPartType:
    session.refresh(scheduled_part, ["part"])
    session.refresh(scheduled_part.part, ["workcenter"])
    session.refresh(scheduled_part.order, ["bill_of_materials"])
    return ScheduledPartType(
        id=scheduled_part.id,
        name=scheduled_part.part.name,
        scheduled_start=scheduled_part.scheduled_start,
        lead_time_seconds=int(scheduled_part.part.lead_time.total_seconds()),
        order=OrderType(
            id=scheduled_part.order_id,
            bill_of_materials=BillOfMaterialsType(
                id=scheduled_part.order.bill_of_materials,
                name=scheduled_part.order.bill_of_materials.name,
            ),
        ),
        part=PartType(
            id=scheduled_part.part.id,
            name=scheduled_part.part.name,
            lead_time_seconds=int(scheduled_part.part.lead_time.total_seconds()),
            workcenter=WorkcenterType(
                id=scheduled_part.part.workcenter.id,
                name=scheduled_part.part.workcenter.name,
            ),
        ),
    )
