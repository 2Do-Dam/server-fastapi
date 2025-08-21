from domain.auth.schemas import UserRegisterRequest, UserLoginRequest, AuthResponse, GoogleLoginRequest, GoogleLoginResponse, LogoutResponse, UserInfo
from domain.users.schemas import UserProfileUpdateRequest
from uuid import uuid4
from datetime import datetime
from infrastructure.security import create_access_token
from fastapi import HTTPException, status
from passlib.context import CryptContext
from domain.users.models import User as UserModel
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def update_user_profile(user_id: str, profile: "UserProfileUpdateRequest", db: Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    user.name = profile.name
    user.nickname = profile.nickname
    user.role = profile.role
    db.commit()
    db.refresh(user)
    return user

def login_user(user: UserLoginRequest, db: Session) -> AuthResponse:
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    # 비밀번호 검증
    if not db_user.password_hash:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    
    if not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    token = create_access_token({"sub": str(db_user.id)})
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=UserInfo(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            nickname=db_user.nickname,
            role=db_user.role,
            created_at=db_user.created_at
        )
    )

def logout_user() -> LogoutResponse:
    return LogoutResponse(message="로그아웃 되었습니다.")

import requests
from core.config import settings
from domain.auth.schemas import GoogleLoginRequest, GoogleLoginResponse, UserInfo
from infrastructure.security import create_access_token
from domain.users.models import User as UserModel
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

def google_login_user(req: GoogleLoginRequest, db: Session) -> GoogleLoginResponse:
    # 1. id_token 검증 (구글 API)
    google_api = f"https://oauth2.googleapis.com/tokeninfo?id_token={req.id_token}"
    resp = requests.get(google_api)
    if resp.status_code != 200:
        raise Exception("Invalid Google token")
    payload = resp.json()
    email = payload["email"]
    name = payload.get("name", "")
    # 2. DB에서 유저 조회/생성
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        user = UserModel(
            id=uuid4(),
            email=email,
            name=name,
            role="youtuber",
            created_at=datetime.utcnow(),
            is_deleted=False
            # password_hash=None (구글 로그인은 비밀번호 없음)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    # 3. JWT 발급
    token = create_access_token({"sub": str(user.id)})
    return GoogleLoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserInfo.model_validate(user)
    )

def create_verified_user(email: str, password: str, name: str = None, nickname: str = None, db: Session = None):
    from domain.users.models import User as UserModel
    from uuid import uuid4
    from datetime import datetime
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # 이메일 중복 체크
    existing = db.query(UserModel).filter(UserModel.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")
    hashed_pw = pwd_context.hash(password)
    user_id = uuid4()
    
    # 이름과 닉네임 설정 (클라이언트에서 받은 값 또는 기본값)
    if not name:
        name = email.split('@')[0]  # 이메일 앞부분을 기본 이름으로
    if not nickname:
        nickname = name  # 이름과 동일하게 설정
    
    db_user = UserModel(
        id=user_id,
        email=email,
        name=name,
        nickname=nickname,
        role="youtuber",  # 기본 역할 설정
        password_hash=hashed_pw,
        created_at=datetime.utcnow(),
        is_deleted=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
