import asyncio
from datetime import timedelta

from src.database import AsyncSession
from src.models import BOMParts
from tests.factories.bill_of_materials import bom_factory
from tests.factories.part import part_factory
from tests.factories.workcenter import workcenter_factory


async def seed_demo_data(db):
    # Create a Bill of Materials for creating a Robot
    bill_of_materials = await bom_factory(name="Robot BoM", session=db)

    # Create workcenters for building all the Robot parts
    arm_workcenter = await workcenter_factory(name="Arm Workcenter", session=db)
    leg_workcenter = await workcenter_factory(name="Leg Workcenter", session=db)
    torso_workcenter = await workcenter_factory(name="Torso Workcenter", session=db)
    cranium_workcenter = await workcenter_factory(name="Cranium Workcenter", session=db)
    eyeball_workcenter = await workcenter_factory(name="Eyeball Workcenter", session=db)

    # Create parts for the Robot
    left_arm = await part_factory(
        name="Left Arm",
        workcenter_id=arm_workcenter.id,
        lead_time=timedelta(days=1),
        session=db,
    )
    right_arm = await part_factory(
        name="Right Arm",
        workcenter_id=arm_workcenter.id,
        lead_time=timedelta(days=1),
        session=db,
    )
    left_leg = await part_factory(
        name="Left Leg",
        workcenter_id=leg_workcenter.id,
        lead_time=timedelta(days=1),
        session=db,
    )
    right_leg = await part_factory(
        name="Right Leg",
        workcenter_id=leg_workcenter.id,
        lead_time=timedelta(days=1),
        session=db,
    )
    torso = await part_factory(
        name="Torso",
        workcenter_id=torso_workcenter.id,
        lead_time=timedelta(days=2),
        session=db,
    )
    cranium = await part_factory(
        name="Cranium",
        workcenter_id=cranium_workcenter.id,
        lead_time=timedelta(days=4),
        session=db,
    )
    eyeball = await part_factory(
        name="Eyeball",
        workcenter_id=eyeball_workcenter.id,
        lead_time=timedelta(days=1),
        session=db,
    )

    # Add parts to the Bill of Materials
    bom_parts = [
        BOMParts(
            part_id=left_arm.id,
            bill_of_materials_id=bill_of_materials.id,
            quantity=1,
        ),
        BOMParts(
            part_id=right_arm.id,
            bill_of_materials_id=bill_of_materials.id,
            quantity=1,
        ),
        BOMParts(
            part_id=right_leg.id,
            bill_of_materials_id=bill_of_materials.id,
            quantity=1,
        ),
        BOMParts(
            part_id=left_leg.id,
            bill_of_materials_id=bill_of_materials.id,
            quantity=1,
        ),
        BOMParts(
            part_id=cranium.id,
            bill_of_materials_id=bill_of_materials.id,
            quantity=1,
        ),
        BOMParts(
            part_id=torso.id,
            bill_of_materials_id=bill_of_materials.id,
            quantity=1,
        ),
        BOMParts(
            part_id=eyeball.id,
            bill_of_materials_id=bill_of_materials.id,
            quantity=2,
        ),
    ]
    db.add_all(bom_parts)
    await db.commit()


async def main():
    async with AsyncSession(expire_on_commit=False) as session:
        await seed_demo_data(session)


if __name__ == "__main__":
    asyncio.run(main())
