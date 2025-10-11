from sqlalchemy import PrimaryKeyConstraint, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

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

    part = relationship("Part", back_populates="bill_of_materials")
    bill_of_materials = relationship("BillOfMaterials", back_populates="parts")

    quantity: Mapped[int] = mapped_column(Integer)
