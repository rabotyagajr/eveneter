from __future__ import annotations

from sqlalchemy import DateTime

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base
from datetime import datetime

if TYPE_CHECKING:
    from eventer.models import Stage


class EventDay(Base):
    __tablename__ = "event_days"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    stage: Mapped["Stage"] = relationship(back_populates="event_day")