from sqlalchemy import Integer, String, Interval, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Part(Base):
    __tablename__ = "parts"

    workcenter_id: Mapped[int] = mapped_column(Integer, ForeignKey("workcenters.id"), index=True)

    workcenter: Mapped["Workcenter"] = relationship("Workcenter", back_populates="parts")  # noqa: F821

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    lead_time: Mapped[Interval] = mapped_column(Interval)
