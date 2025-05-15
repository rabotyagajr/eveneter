from pydantic import BaseModel
from typing import Optional
from eventer.enums import UserStatus, Role


class EventMemberBase(BaseModel):
    user_status: UserStatus = UserStatus.PENDING
    role: Role = Role.USER


class EventMemberCreate(EventMemberBase):
    user_id: int
    event_id: int


class EventMemberUpdate(BaseModel):
    user_status: Optional[UserStatus] = None
    role: Optional[Role] = None


class EventMemberRead(EventMemberBase):
    user_id: int
    event_id: int

    class Config:
        from_attributes = True
