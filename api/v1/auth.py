from fastapi import APIRouter, Depends
from domain.auth.schemas import UserRegisterRequest, UserLoginRequest, AuthResponse, GoogleLoginRequest, GoogleLoginResponse, LogoutResponse
from infrastructure.security import get_current_user
from domain.auth.services import register_user, login_user, logout_user, google_login_user
from infrastructure.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register", response_model=AuthResponse)
def register(user: UserRegisterRequest, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login", response_model=AuthResponse)
def login(user: UserLoginRequest, db: Session = Depends(get_db)):
    return login_user(user, db)

@router.post("/logout", response_model=LogoutResponse)
def logout(current_user=Depends(get_current_user)):
    return logout_user()

@router.post("/google", response_model=GoogleLoginResponse)
def google_login(req: GoogleLoginRequest):
    return google_login_user(req)
