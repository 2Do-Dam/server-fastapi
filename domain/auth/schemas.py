from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str = email.split('@')[0]
    nickname: Optional[str] = None



class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class GoogleLoginRequest(BaseModel):
    id_token: str


class UserInfo(BaseModel):
    id: UUID
    email: EmailStr
    name: str = ""
    nickname: Optional[str] = None
    role: Optional[str] = None
    created_at: datetime

class GoogleLoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserInfo

class LogoutResponse(BaseModel):
    message: str
class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserInfo
