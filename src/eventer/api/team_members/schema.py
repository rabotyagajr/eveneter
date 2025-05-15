from pydantic import BaseModel
from typing import Optional


class TeamMemberBase(BaseModel):
    team_id: int
    user_id: int
    is_leader: bool = False
    is_active: bool = True

class TeamMemberRead(TeamMemberBase):
    pass

class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMemberUpdate(BaseModel):
    team_id: Optional[int] = None
    is_leader: Optional[bool] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True
