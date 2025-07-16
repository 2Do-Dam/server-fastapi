from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str

class UserProfileUpdateRequest(BaseModel):
    name: str
    nickname: str
    role: Optional[str] = "youtuber"

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class GoogleLoginRequest(BaseModel):
    id_token: str


class UserInfo(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

class GoogleLoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserInfo

class LogoutResponse(BaseModel):
    message: str
class AuthResponse(BaseModel):
    token_type: str
    user: UserInfo
