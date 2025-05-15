from __future__ import annotations

from sqlalchemy import ForeignKey

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base
from sqlalchemy.dialects.postgresql import ENUM as PgENUM
from eventer.enums import Role, UserStatus

if TYPE_CHECKING:
    from eventer.models import User

class EventMember(Base):
    __tablename__ = "event_members"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), primary_key=True
    )
    user_status: Mapped[UserStatus] = mapped_column(
        PgENUM(UserStatus, name="users_status"),
        nullable=False,
        default=UserStatus.PENDING,
    )
    role: Mapped[Role] = mapped_column(
        PgENUM(Role, name="user_role"),
        nullable=False,
        default=Role.USER,
    )

    event = relationship("Event", back_populates="event_members")
    user: Mapped["User"] = relationship(back_populates="event_memberships")