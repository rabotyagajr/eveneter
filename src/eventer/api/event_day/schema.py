from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class EventDayBase(BaseModel):
    start_time: datetime = Field(...)
    end_time: datetime = Field(...)


class EventDayCreate(EventDayBase):
    pass


class EventDayUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class EventDayRead(EventDayBase):
    id: int

    class Config:
        from_attributes = True
