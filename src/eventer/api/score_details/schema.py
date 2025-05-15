from decimal import Decimal
from pydantic import BaseModel, Field


class ScoreDetailBase(BaseModel):
    score: Decimal = Field(...)


class ScoreDetailCreate(ScoreDetailBase):
    stage_score_id: int = Field(..., description="ID общей оценки этапа")
    parameter_id: int = Field(..., description="ID параметра оценки")
    judge_id: int = Field(..., description="ID судьи")


class ScoreDetailUpdate(BaseModel):
    score: Decimal = Field(None)


class ScoreDetailRead(ScoreDetailBase):
    id: int
    stage_score_id: int
    parameter_id: int
    judge_id: int

    class Config:
        from_attributes = True
