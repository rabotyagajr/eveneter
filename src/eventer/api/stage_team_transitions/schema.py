from pydantic import BaseModel, Field
from typing import Optional


class StageTeamTransitionBase(BaseModel):
    team_id: int = Field(...)
    from_stage_id: int = Field(...)
    to_stage_id: int = Field(...)


class StageTeamTransitionCreate(StageTeamTransitionBase):
    pass


class StageTeamTransitionUpdate(BaseModel):
    team_id: Optional[int] = Field(None)
    from_stage_id: Optional[int] = Field(None)
    to_stage_id: Optional[int] = Field(None)


class StageTeamTransitionRead(StageTeamTransitionBase):
    id: int

    class Config:
        from_attributes = True
