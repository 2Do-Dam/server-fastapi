from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str
    nickname: Optional[str] = None
    role: Optional[str] = "youtuber"
    profile_image: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    created_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True

class UserProfileUpdateRequest(BaseModel):
    name: str
    nickname: str
    role: Optional[str] = "youtuber"

class UserRoleUpdateRequest(BaseModel):
    roles: List[str]

class UserRole(BaseModel):
    user_id: UUID
    role: str
    class Config:
        from_attributes = True
