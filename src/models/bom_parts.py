from sqlalchemy import PrimaryKeyConstraint, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base


class BOMParts(Base):
    __tablename__ = "boms_parts"
    __table_args__ = (PrimaryKeyConstraint("part_id", "bill_of_materials_id"),)

    part_id: Mapped[int] = mapped_column(
        ForeignKey("parts.id"),
    )
    bill_of_materials_id: Mapped[int] = mapped_column(
        ForeignKey("bill_of_materials.id"),
    )

    part = relationship("Part", back_populates="bom_parts")
    bill_of_materials = relationship("BillOfMaterials", back_populates="bom_parts")

    quantity: Mapped[int] = mapped_column(Integer)
