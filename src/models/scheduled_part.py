from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, PrimaryKeyConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .part import Part
    from .order import Order


class ScheduledPart(Base):
    __tablename__ = "scheduled_parts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    part_id: Mapped[int] = mapped_column(
        ForeignKey("parts.id"),
        nullable=False,
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )

    part: Mapped["Part"] = relationship("Part", back_populates="scheduled_parts")
    order: Mapped["Order"] = relationship("Order", back_populates="scheduled_parts")

    scheduled_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
