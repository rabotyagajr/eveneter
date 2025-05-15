from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from eventer.enums import EventFormat, Status


class EventBase(BaseModel):
    event_name: str
    description: str
    image_url: str
    users_count: int = Field(ge=0)
    format: EventFormat
    venue: str
    start_date: datetime
    end_date: datetime
    event_status: Status = Status.ACTIVE

class EventCreate(EventBase):
    organizer_id: int
    category_id: int


class EventUpdate(BaseModel):
    event_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    users_count: Optional[int] = Field(None, ge=0)
    format: Optional[EventFormat] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    event_status: Optional[Status] = None

class EventRead(EventBase):
    id: int
    organizer_id: int
    category_id: int
    class Config:
        from_attributes = True

class EventRecent(BaseModel):
    id: int
    event_name: str
    format: EventFormat
    image_url: str
    venue: str
    start_date: datetime
    end_date: datetime
    event_status: Status