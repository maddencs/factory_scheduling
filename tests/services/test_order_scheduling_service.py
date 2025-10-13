from datetime import timedelta

import pytest
from sqlalchemy import select

from src.models import ScheduledPart
from src.services.order_scheduling import OrderScheduler
from tests.factories.bill_of_materials import bom_factory
from tests.factories.bom_part import bom_part_factory
from tests.factories.order import order_factory
from tests.factories.part import part_factory
from tests.factories.workcenter import workcenter_factory


@pytest.mark.asyncio
async def test_order_service_schedule_parts__free_workcenter(db_session):
    """
    Schedule parts for a workcenter that doesn't have any active scheduled parts
    """
    workcenter = await workcenter_factory(
        session=db_session,
        name="Robot Workcenter",
    )
    bom = await bom_factory(
        session=db_session,
        name="Robot",
    )
    lead_time = timedelta(days=1)
    part = await part_factory(
        name="Left Arm",
        lead_time=lead_time,
        workcenter_id=workcenter.id,
        session=db_session,
    )
    await bom_part_factory(
        part_id=part.id,
        bill_of_materials_id=bom.id,
        quantity=1,
        session=db_session,
    )

    order = await order_factory(bill_of_materials_id=bom.id, session=db_session)

    await OrderScheduler().schedule(order, db_session)

    result = await db_session.execute(select(ScheduledPart))
    scheduled_part = result.scalar_one()

    assert scheduled_part.part_id == part.id
    assert scheduled_part.order_id == order.id
    assert scheduled_part.scheduled_start is not None


@pytest.mark.asyncio
async def test_order_service_schedule_parts__workcenter_with_one_scheduled_part(db_session):
    """
    Schedule a part for a workcenter that has one scheduled part
    """
    workcenter = await workcenter_factory(
        session=db_session,
        name="Robot Workcenter",
    )
    bom = await bom_factory(
        session=db_session,
        name="Robot",
    )
    lead_time = timedelta(days=1)
    part = await part_factory(
        name="Left Arm",
        lead_time=lead_time,
        workcenter_id=workcenter.id,
        session=db_session,
    )
    await bom_part_factory(
        part_id=part.id,
        bill_of_materials_id=bom.id,
        quantity=1,
        session=db_session,
    )

    prior_order = await order_factory(bill_of_materials_id=bom.id, session=db_session)
    new_order = await order_factory(bill_of_materials_id=bom.id, session=db_session)

    await OrderScheduler().schedule(prior_order, db_session)
    await OrderScheduler().schedule(new_order, db_session)

    result = await db_session.execute(select(ScheduledPart).order_by(ScheduledPart.scheduled_start.asc()))
    scheduled_parts = result.scalars().all()
    prior_scheduled_part = scheduled_parts[0]
    new_scheduled_part = scheduled_parts[1]

    assert prior_scheduled_part.part_id == part.id
    assert prior_scheduled_part.order_id == prior_order.id
    assert prior_scheduled_part.scheduled_start is not None

    assert new_scheduled_part.part_id == part.id
    assert new_scheduled_part.order_id == new_order.id
    assert new_scheduled_part.scheduled_start is not None
    assert new_scheduled_part.scheduled_start == prior_scheduled_part.scheduled_start + part.lead_time


@pytest.mark.asyncio
async def test_order_service_schedule_parts__multi_workcenter(db_session):
    """
    Schedule parts of different lead times for two workcenters that don't have any active scheduled parts
    """
    cranium_workcenter = await workcenter_factory(
        session=db_session,
        name="Cranium Workcenter",
    )
    torso_workcenter = await workcenter_factory(
        session=db_session,
        name="Torso Workcenter",
    )
    bom = await bom_factory(
        session=db_session,
        name="Robot",
    )
    cranium_lead_time = timedelta(days=1)
    cranium_part = await part_factory(
        name="Cranium",
        lead_time=cranium_lead_time,
        workcenter_id=cranium_workcenter.id,
        session=db_session,
    )
    await bom_part_factory(
        part_id=cranium_part.id,
        bill_of_materials_id=bom.id,
        quantity=1,
        session=db_session,
    )

    torso_lead_time = timedelta(days=2)
    torso_part = await part_factory(
        name="Cranium",
        lead_time=torso_lead_time,
        workcenter_id=torso_workcenter.id,
        session=db_session,
    )
    await bom_part_factory(
        part_id=torso_part.id,
        bill_of_materials_id=bom.id,
        quantity=1,
        session=db_session,
    )

    order = await order_factory(bill_of_materials_id=bom.id, session=db_session)

    await OrderScheduler().schedule(order, db_session)

    result = await db_session.execute(select(ScheduledPart))
    scheduled_parts = result.scalars().all()
    torso_scheduled_part = [sp for sp in scheduled_parts if sp.part_id == torso_part.id][0]
    cranium_scheduled_part = [sp for sp in scheduled_parts if sp.part_id == cranium_part.id][0]

    assert cranium_scheduled_part.scheduled_start == (
        torso_scheduled_part.scheduled_start + torso_lead_time - cranium_lead_time
    )
