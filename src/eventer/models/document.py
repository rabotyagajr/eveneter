from __future__ import annotations

from sqlalchemy import String, ForeignKey, Text

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base

if TYPE_CHECKING:
    from eventer.models import Event

class Document(Base):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))

    event: Mapped["Event"] = relationship(back_populates="documents")