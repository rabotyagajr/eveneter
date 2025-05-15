from pydantic import BaseModel, Field
from typing import Optional


class EventTeamBase(BaseModel):
    team_id: int = Field(...)
    event_id: int = Field(...)


class EventTeamCreate(EventTeamBase):
    pass


class EventTeamUpdate(BaseModel):
    team_id: Optional[int] = Field(None)
    event_id: Optional[int] = Field(None)


class EventTeamRead(EventTeamBase):
    id: int

    class Config:
        from_attributes = True
