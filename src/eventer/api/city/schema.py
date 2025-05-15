from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class CityBase(BaseModel):
    name: str = Field(..., max_length=100)


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str = Field(None, max_length=100)


class CityRead(CityBase):
    id: int

    class Config:
        from_attributes = True
