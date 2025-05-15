from __future__ import annotations

from sqlalchemy import ForeignKey, Numeric
from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base

if TYPE_CHECKING:
    from eventer.models import Team, Stage, ScoreDetail


class StageScore(Base):
    __tablename__ = "stage_scores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    total_score: Mapped[Decimal] = mapped_column(
        Numeric(precision=5, scale=2), nullable=False
    )
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    stage_id: Mapped[int] = mapped_column(ForeignKey("stages.id", ondelete="CASCADE"))

    team: Mapped["Team"] = relationship(back_populates="scores")
    stage: Mapped["Stage"] = relationship(back_populates="scores")
    details: Mapped[list["ScoreDetail"]] = relationship(back_populates="stage_score")
