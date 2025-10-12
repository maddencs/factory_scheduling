from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .bill_of_materials import BillOfMaterials
    from .scheduled_part import ScheduledPart


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bill_of_materials_id: Mapped[int] = mapped_column(ForeignKey("bill_of_materials.id"))

    bill_of_materials: Mapped["BillOfMaterials"] = relationship("BillOfMaterials", back_populates="orders")
    scheduled_parts: Mapped[list["ScheduledPart"]] = relationship("ScheduledPart", back_populates="order")
