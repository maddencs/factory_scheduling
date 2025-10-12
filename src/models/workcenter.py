from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .part import Part


class Workcenter(Base):
    __tablename__ = "workcenters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    parts: Mapped[List["Part"]] = relationship(
        "Part",
        back_populates="workcenter",
    )
