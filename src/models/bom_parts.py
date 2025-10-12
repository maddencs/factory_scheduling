from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .bill_of_materials import BillOfMaterials
    from .part import Part


class BOMParts(Base):
    __tablename__ = "boms_parts"
    __table_args__ = (PrimaryKeyConstraint("part_id", "bill_of_materials_id"),)

    part_id: Mapped[int] = mapped_column(
        ForeignKey("parts.id"),
    )
    bill_of_materials_id: Mapped[int] = mapped_column(
        ForeignKey("bill_of_materials.id"),
    )

    part: Mapped["Part"] = relationship("Part", back_populates="bom_parts")
    bill_of_materials: Mapped["BillOfMaterials"] = relationship("BillOfMaterials", back_populates="bom_parts")

    quantity: Mapped[int] = mapped_column(Integer)
