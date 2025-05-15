from pydantic import BaseModel, Field
from typing import Optional
from eventer.enums import CertificateType


class CertificateBase(BaseModel):
    type: CertificateType = Field(...)
    file_path: str = Field(..., max_length=500)


class CertificateCreate(CertificateBase):
    event_id: int = Field(...)
    stage_id: int = Field(...)
    user_id: int = Field(...)


class CertificateUpdate(BaseModel):
    type: Optional[CertificateType] = Field(None)
    file_path: Optional[str] = Field(None, max_length=500)


class CertificateRead(CertificateBase):
    id: int
    event_id: int
    stage_id: int
    user_id: int

    class Config:
        from_attributes = True
