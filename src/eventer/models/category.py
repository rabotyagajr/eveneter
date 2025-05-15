from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from eventer.models.base.base import Base

if TYPE_CHECKING:
    from eventer.models import Event

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    
    events: Mapped[list["Event"]] = relationship(back_populates="category")