import datetime
from collections import defaultdict
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Order, Part, ScheduledPart


async def submit_order(
    bill_of_materials_id: int,
    session: AsyncSession,
) -> Order:
    order = Order(
        bill_of_materials_id=bill_of_materials_id,
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)

    await schedule_parts(order, session)

    return order


async def refresh_order_related_objects(order: Order, session: AsyncSession):
    await session.refresh(order, ["bill_of_materials"])
    await session.refresh(order.bill_of_materials, ["bom_parts"])

    for bom_part in order.bill_of_materials.bom_parts:
        await session.refresh(bom_part, ["part"])
        await session.refresh(bom_part.part, ["workcenter"])


async def schedule_parts(order: Order, session: AsyncSession):
    await refresh_order_related_objects(order, session)

    parts_by_workcenter = defaultdict(list)
    for bom_part in order.bill_of_materials.bom_parts:
        parts_by_workcenter[bom_part.part.workcenter].append(bom_part)

    maximum_end_time = await get_maximum_end_time(parts_by_workcenter, session)
    for workcenter, bom_parts in parts_by_workcenter.items():
        workcenter_current_end_time = maximum_end_time or datetime.datetime.now() + datetime.timedelta(
            seconds=sum(bom_part.quantity * bom_part.part.lead_time.total_seconds() for bom_part in bom_parts)
        )
        for bom_part in bom_parts:
            for i in range(bom_part.quantity):
                start_time = workcenter_current_end_time - bom_part.part.lead_time
                workcenter_current_end_time = start_time
                session.add(
                    ScheduledPart(
                        part_id=bom_part.part_id,
                        order_id=order.id,
                        scheduled_start=start_time,
                    )
                )

    await session.commit()


async def get_maximum_end_time(
    parts_by_workcenter: defaultdict[Any, list], session: AsyncSession
) -> datetime.datetime | None:
    end_times = list()
    for workcenter, bom_parts in parts_by_workcenter.items():
        wc_last_scheduled_part = await session.execute(
            select(ScheduledPart)
            .join(ScheduledPart.part)
            .options(selectinload(ScheduledPart.part))
            .where(Part.workcenter_id == workcenter.id)
            .order_by(ScheduledPart.scheduled_start.asc())
        )
        wc_last_scheduled_part = wc_last_scheduled_part.scalar_one_or_none()
        total_new_work = sum(bom_part.quantity * bom_part.part.lead_time.total_seconds() for bom_part in bom_parts)
        if wc_last_scheduled_part:
            end_times.append(
                wc_last_scheduled_part.scheduled_start
                + wc_last_scheduled_part.part.lead_time
                + datetime.timedelta(seconds=total_new_work)
            )
        else:
            end_times.append(datetime.datetime.now() + datetime.timedelta(seconds=total_new_work))
    return max(end_times) if end_times else None
