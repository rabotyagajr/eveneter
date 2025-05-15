from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from eventer.enums import Role, Gender


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    role: Role = Role.USER
    gender: Optional[Gender] = None
    age: Optional[int] = None
    city_id: Optional[int] = None


class UserCreate(UserBase):
    sub_token: str
    email: EmailStr
    firstname: str
    lastname: str


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
