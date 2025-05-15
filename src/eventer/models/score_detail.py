from __future__ import annotations

from sqlalchemy import ForeignKey, Numeric
from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base

if TYPE_CHECKING:
    from eventer.models import User, StageScore, Parameter
    
class ScoreDetail(Base):
    __tablename__ = "score_details"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stage_score_id: Mapped[int] = mapped_column(
        ForeignKey("stage_scores.id", ondelete="CASCADE")
    )
    parameter_id: Mapped[int] = mapped_column(
        ForeignKey("parameters.id", ondelete="CASCADE")
    )
    judge_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    score: Mapped[Decimal] = mapped_column(
        Numeric(precision=5, scale=2), nullable=False
    )

    stage_score: Mapped["StageScore"] = relationship(back_populates="details")
    parameter: Mapped["Parameter"] = relationship(back_populates="scores")
    judge: Mapped["User"] = relationship(back_populates="scores_given")