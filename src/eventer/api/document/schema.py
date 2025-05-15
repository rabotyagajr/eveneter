from pydantic import BaseModel, Field
from typing import Optional


class DocumentBase(BaseModel):
    name: str = Field(..., max_length=255)
    content: str = Field(...)


class DocumentCreate(DocumentBase):
    event_id: int = Field(...)


class DocumentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = Field(None)


class DocumentRead(DocumentBase):
    id: int
    event_id: int

    class Config:
        from_attributes = True
