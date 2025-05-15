from __future__ import annotations

from sqlalchemy import ForeignKey, String, Integer
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base

if TYPE_CHECKING:
    from eventer.models import Event, ScoreDetail


class Parameter(Base):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    parameter_name: Mapped[str] = mapped_column(String(255), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    max_score: Mapped[int] = mapped_column(Integer(), nullable=False)

    event: Mapped["Event"] = relationship(back_populates="parameters")
    scores: Mapped[list["ScoreDetail"]] = relationship(back_populates="parameter")
