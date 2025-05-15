from pydantic import BaseModel, Field
from typing import Optional


class TeamBase(BaseModel):
    team_name: str = Field(..., max_length=70)
    logo: str = Field(..., max_length=45)
    description: str = Field(
        ...,
    )


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    team_name: Optional[str] = Field(None, max_length=70)
    logo: Optional[str] = Field(None, max_length=45)
    description: Optional[str] = None


class TeamRead(TeamBase):
    id: int

    class Config:
        from_attributes = True
