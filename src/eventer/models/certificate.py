from __future__ import annotations

from sqlalchemy import ForeignKey, String

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base
from eventer.enums import CertificateType
from sqlalchemy.dialects.postgresql import ENUM as PgENUM

if TYPE_CHECKING:
    from eventer.models import Event, Stage, User


class Certificate(Base):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    type: Mapped[CertificateType] = mapped_column(
        PgENUM(CertificateType), nullable=False
    )
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    stage_id: Mapped[int] = mapped_column(ForeignKey("stages.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    event: Mapped["Event"] = relationship(back_populates="certificates")
    stage: Mapped["Stage"] = relationship(back_populates="certificates")
    user: Mapped["User"] = relationship(back_populates="certificates")
