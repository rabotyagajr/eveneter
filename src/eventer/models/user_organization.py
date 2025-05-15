from sqlalchemy import ForeignKey, Table, Column
from eventer.models.base.base import Base

user_organization = Table(
    "user_organization",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("users.id"),
        primary_key=True,
    ),
    Column(
        "organization_id",
        ForeignKey("organizations.id"),
        primary_key=True,
    ),
)
