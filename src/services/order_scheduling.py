import datetime
from collections import defaultdict
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Order, Part, ScheduledPart


class OrderScheduleRunner:
    """Order scheduling runner to make it easy to implement asynchronous scheduling later"""

    def __init__(self, scheduler: "OrderScheduler", session: AsyncSession):
        self.session = session
        self.scheduler = scheduler

    async def run(self, order: Order):
        await self.scheduler.schedule(order, self.session)

    def run_async(self, order: Order):
        raise NotImplementedError("Asynchronous scheduling is not yet implemented.")


class OrderScheduler:
    async def schedule(self, order: Order, session: AsyncSession):
        await session.refresh(order, ["bill_of_materials"])
        await session.refresh(order.bill_of_materials, ["bom_parts"])

        for bom_part in order.bill_of_materials.bom_parts:
            await session.refresh(bom_part, ["part"])
            await session.refresh(bom_part.part, ["workcenter"])

        await self._schedule_parts(order, session)

    async def _schedule_parts(self, order: Order, session: AsyncSession):
        parts_by_workcenter = defaultdict(list)
        for bom_part in order.bill_of_materials.bom_parts:
            parts_by_workcenter[bom_part.part.workcenter].append(bom_part)

        maximum_end_time = await self._get_maximum_end_time(parts_by_workcenter, session)
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

    async def _get_maximum_end_time(
        self,
        parts_by_workcenter: defaultdict[Any, list],
        session: AsyncSession,
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
