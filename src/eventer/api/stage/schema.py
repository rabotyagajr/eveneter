from eventer.enums import Status, StageType
from pydantic import BaseModel, Field
from typing import Optional


class StageBase(BaseModel):
    stage_name: str = Field(...)
    description: Optional[str] = Field(None)
    type: StageType = Field(...)
    users_on_stage: int = Field(0, ge=0)
    stage_status: Status = Field(Status.ACTIVE)


class StageCreate(StageBase):
    event_id: int = Field(...)
    event_day_id: int = Field(...)


class StageUpdate(BaseModel):
    stage_name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    type: Optional[StageType] = Field(None)
    users_on_stage: Optional[int] = Field(None, ge=0)
    stage_status: Optional[Status] = Field(None)
    event_day_id: Optional[int] = Field(None)


class StageRead(StageBase):
    id: int
    event_id: int
    event_day_id: int

    class Config:
        from_attributes = True
