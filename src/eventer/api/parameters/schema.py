from pydantic import BaseModel, Field
from typing import Optional


class ParameterBase(BaseModel):
    parameter_name: str = Field(...)
    max_score: int = Field(...)


class ParameterCreate(ParameterBase):
    event_id: int = Field(...)


class ParameterUpdate(BaseModel):
    parameter_name: Optional[str] = Field(None)
    max_score: Optional[int] = Field(None)


class ParameterRead(ParameterBase):
    id: int
    event_id: int

    class Config:
        from_attributes = True
