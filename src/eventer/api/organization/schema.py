from pydantic import BaseModel, Field
from typing import Optional


class OrganizationBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str = Field(...)


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None)


class OrganizationRead(OrganizationBase):
    id: int

    class Config:
        from_attributes = True
