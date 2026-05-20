from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class PainPointRequest(BaseModel):
    pain_points: List[str]


class BusinessDataResponse(BaseModel):
    id: int
    title: str
    filename: str
    summary: Optional[str]
    uploaded_at: datetime

    class Config:
        orm_mode = True
