from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    DateTime,
    Text,
    Integer,
)
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base
from eventer.enums import EventFormat, Status
from sqlalchemy.dialects.postgresql import ENUM as PgENUM
from datetime import datetime

if TYPE_CHECKING:
    from eventer.models import (
        User,
        Stage,
        Category,
        EventMember,
        Document,
        EventTeam,
        Parameter,
        Certificate,
        LeaderBoard,
    )


class Event(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_name: Mapped[str] = mapped_column(Text())
    image_url: Mapped[str] = mapped_column("image_path", String(255), nullable=True)
    venue: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())
    users_count: Mapped[int] = mapped_column(Integer())
    format: Mapped[EventFormat] = mapped_column(
        PgENUM(EventFormat, name="event_format")
    )
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )
    organizer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    event_status: Mapped[Status] = mapped_column(default=Status.ACTIVE)

    organizer: Mapped["User"] = relationship(back_populates="organized_events")
    stages: Mapped["Stage"] = relationship(back_populates="event")
    event_members: Mapped[list[EventMember]] = relationship(back_populates="event")
    documents: Mapped[list["Document"]] = relationship(back_populates="event")
    team_associations: Mapped[list["EventTeam"]] = relationship(back_populates="event")
    parameters: Mapped[list["Parameter"]] = relationship(back_populates="event")
    certificates: Mapped[list["Certificate"]] = relationship(back_populates="event")
    leaderboard_entries: Mapped[list["LeaderBoard"]] = relationship(
        back_populates="event"
    )
    category: Mapped["Category"] = relationship(back_populates="events")