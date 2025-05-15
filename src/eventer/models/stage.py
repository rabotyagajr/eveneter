from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models import Base
from sqlalchemy.dialects.postgresql import ENUM as PgENUM
from eventer.enums import StageType, Status

if TYPE_CHECKING:
    from eventer.models import (
        Event,
        EventDay,
        StageTeamTransition,
        StageScore,
        Certificate,
    )


class Stage(Base):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stage_name: Mapped[str] = mapped_column(Text(), nullable=False)
    description: Mapped[str] = mapped_column(Text())
    type: Mapped[StageType] = mapped_column(PgENUM(StageType, name="stage_type"))
    users_on_stage: Mapped[int] = mapped_column(Integer(), default=0)
    event_day_id: Mapped[int] = mapped_column(
        ForeignKey("event_days.id", ondelete="CASCADE")
    )
    stage_status: Mapped[Status] = mapped_column(default=Status.ACTIVE)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))

    event: Mapped["Event"] = relationship(back_populates="stages")
    event_day: Mapped["EventDay"] = relationship(back_populates="stage")
    from_transitions: Mapped[list["StageTeamTransition"]] = relationship(
        back_populates="from_stage", foreign_keys="StageTeamTransition.from_stage_id"
    )
    to_transitions: Mapped[list["StageTeamTransition"]] = relationship(
        back_populates="to_stage", foreign_keys="StageTeamTransition.to_stage_id"
    )
    scores: Mapped[list["StageScore"]] = relationship(back_populates="stage")
    certificates: Mapped[list["Certificate"]] = relationship(back_populates="stage")
