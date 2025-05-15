from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base

if TYPE_CHECKING:
    from eventer.models import Team, User


class TeamMember(Base):
    __tablename__ = "team_members"

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    is_leader: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    team: Mapped["Team"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="team_memberships")
