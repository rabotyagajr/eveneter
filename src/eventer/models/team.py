from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models import Base

if TYPE_CHECKING:
    from eventer.models import (
        StageTeamTransition,
        StageScore,
        TeamMember,
        EventTeam,
        LeaderBoard,
    )


class Team(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    team_name: Mapped[str] = mapped_column(String(70))
    logo: Mapped[str] = mapped_column(String(45))
    description: Mapped[str] = mapped_column(Text())

    members: Mapped[list["TeamMember"]] = relationship(back_populates="team")
    transitions: Mapped[list["StageTeamTransition"]] = relationship(
        back_populates="team"
    )
    event_associations: Mapped[list["EventTeam"]] = relationship(back_populates="team")
    scores: Mapped[list["StageScore"]] = relationship(back_populates="team")
    leaderboard_entries: Mapped[list["LeaderBoard"]] = relationship(
        back_populates="team"
    )
