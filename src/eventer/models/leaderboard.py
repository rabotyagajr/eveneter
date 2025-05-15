from __future__ import annotations

from sqlalchemy import ForeignKey, Numeric
from typing import TYPE_CHECKING

from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models import Base

if TYPE_CHECKING:
    from eventer.models import Event, Team
    
class LeaderBoard(Base):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    total_score: Mapped[Decimal] = mapped_column(
        Numeric(precision=4, scale=2), nullable=False, default=Decimal("0.00")
    )
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))

    event: Mapped["Event"] = relationship(back_populates="leaderboard_entries")
    team: Mapped["Team"] = relationship(back_populates="leaderboard_entries")