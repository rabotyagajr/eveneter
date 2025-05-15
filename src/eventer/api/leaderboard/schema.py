from decimal import Decimal
from pydantic import BaseModel, Field


class LeaderBoardBase(BaseModel):
    total_score: Decimal = Field(default=Decimal("0.00"))


class LeaderBoardCreate(LeaderBoardBase):
    event_id: int = Field(...)
    team_id: int = Field(...)


class LeaderBoardUpdate(BaseModel):
    total_score: Decimal = Field(None)


class LeaderBoardRead(LeaderBoardBase):
    id: int
    event_id: int
    team_id: int

    class Config:
        from_attributes = True
