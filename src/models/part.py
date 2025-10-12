from datetime import timedelta
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, Interval, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .bill_of_materials import BillOfMaterials
    from .bom_parts import BOMParts
    from .workcenter import Workcenter
    from .scheduled_part import ScheduledPart


class Part(Base):
    __tablename__ = "parts"

    workcenter_id: Mapped[int] = mapped_column(Integer, ForeignKey("workcenters.id"), index=True)

    workcenter: Mapped["Workcenter"] = relationship("Workcenter", back_populates="parts")

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    lead_time: Mapped[timedelta] = mapped_column(Interval)

    bom_parts: Mapped[List["BOMParts"]] = relationship("BOMParts", back_populates="part")
    bills_of_materials: Mapped[List["BillOfMaterials"]] = relationship(
        "BillOfMaterials",
        back_populates="parts",
        secondary="boms_parts",
        viewonly=True,
    )
    scheduled_parts: Mapped[list["ScheduledPart"]] = relationship("ScheduledPart", back_populates="part")
