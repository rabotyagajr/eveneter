from __future__ import annotations

from sqlalchemy import String

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eventer.models.base.base import Base

if TYPE_CHECKING:
    from eventer.models import User


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    users: Mapped[list["User"]] = relationship(back_populates="city")
