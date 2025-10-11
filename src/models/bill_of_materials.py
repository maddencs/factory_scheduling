from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .order import Order
    from .bom_parts import BOMParts


class BillOfMaterials(Base):
    __tablename__ = "bill_of_materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="bill_of_materials",
    )

    bom_parts: Mapped[list["BOMParts"]] = relationship(
        "BOMParts",
        back_populates="bill_of_materials",
    )
    parts: Mapped[list["BOMParts"]] = relationship(
        "Part",
        secondary="boms_parts",
        viewonly=True,
    )
