from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .bill_of_materials import BillOfMaterials


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bill_of_materials_id: Mapped[int] = mapped_column(ForeignKey("bill_of_materials.id"))
    workcenter_id: Mapped[int] = mapped_column(ForeignKey("workcenters.id"))

    bill_of_materials: Mapped["BillOfMaterials"] = relationship("BillOfMaterials", back_populates="orders")
