from __future__ import annotations
from sqlalchemy import ForeignKey, String, DateTime

from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models import Base
from eventer.enums import Role, Gender
from sqlalchemy.dialects.postgresql import ENUM as PgENUM
from datetime import datetime, timezone
from .user_organization import user_organization

if TYPE_CHECKING:
    from eventer.models import (
        Organization,
        Event,
        EventMember,
        TeamMember,
        ScoreDetail,
        Certificate,
        City,
    )


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sub_token: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(45))
    firstname: Mapped[str] = mapped_column(String(45))
    lastname: Mapped[str] = mapped_column(String(45))
    role: Mapped[Role] = mapped_column(
        PgENUM(Role, name="user_role"), nullable=False, default=Role.USER
    )
    gender: Mapped[Gender] = mapped_column(PgENUM(Gender, name="user_gender"))
    age: Mapped[int]
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    organizations: Mapped[list["Organization"]] = relationship(
        secondary=user_organization,
        back_populates="members",
        cascade="all, delete",
    )
    city_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"), nullable=True
    )
    city: Mapped["City"] = relationship(back_populates="users")
    organized_events: Mapped[list["Event"]] = relationship(back_populates="organizer")

    event_memberships: Mapped[list["EventMember"]] = relationship(back_populates="user")

    team_memberships: Mapped[list["TeamMember"]] = relationship(back_populates="user")
    scores_given: Mapped[list["ScoreDetail"]] = relationship(back_populates="judge")
    certificates: Mapped[list["Certificate"]] = relationship(back_populates="user")
