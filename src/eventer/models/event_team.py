from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base

if TYPE_CHECKING:
    from eventer.models import Event, Team

class EventTeam(Base):
    __tablename__ = "event_teams"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))

    team: Mapped["Team"] = relationship(back_populates="event_associations")
    event: Mapped["Event"] = relationship(back_populates="team_associations")