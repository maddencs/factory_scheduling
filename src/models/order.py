from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from .base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bill_of_materials_id: Mapped[int] = mapped_column(ForeignKey("bill_of_materials.id"))
    workcenter_id: Mapped[int] = mapped_column(ForeignKey("workcenters.id"))

    bill_of_material = relationship("BillOfMaterials", back_populates="orders")
