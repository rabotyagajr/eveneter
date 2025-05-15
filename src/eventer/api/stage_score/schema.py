from decimal import Decimal
from pydantic import BaseModel, Field


class StageScoreBase(BaseModel):
    total_score: Decimal = Field(...)


class StageScoreCreate(StageScoreBase):
    team_id: int = Field(...)
    stage_id: int = Field(...)


class StageScoreUpdate(BaseModel):
    total_score: Decimal = Field(None)


class StageScoreRead(StageScoreBase):
    id: int
    team_id: int
    stage_id: int

    class Config:
        from_attributes = True
