from __future__ import annotations

from sqlalchemy import String, DateTime, Text
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base
from datetime import datetime, timezone
from .user_organization import user_organization

if TYPE_CHECKING:
    from eventer.models import User

class Organization(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    members: Mapped[list["User"]] = relationship(
        secondary=user_organization,
        back_populates="organizations",
        cascade="all, delete",
    )