from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base

if TYPE_CHECKING:
    from eventer.models import Team, Stage


class StageTeamTransition(Base):
    __tablename__ = "stage_team_transitions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    from_stage_id: Mapped[int] = mapped_column(
        ForeignKey("stages.id", ondelete="CASCADE")
    )
    to_stage_id: Mapped[int] = mapped_column(
        ForeignKey("stages.id", ondelete="CASCADE")
    )

    team: Mapped["Team"] = relationship(back_populates="transitions")
    from_stage: Mapped["Stage"] = relationship(
        foreign_keys=[from_stage_id], back_populates="from_transitions"
    )
    to_stage: Mapped["Stage"] = relationship(foreign_keys=[to_stage_id])