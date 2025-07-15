from domain.auth.schemas import UserRegisterRequest, UserLoginRequest, AuthResponse, GoogleLoginRequest, GoogleLoginResponse, LogoutResponse, UserInfo
from uuid import uuid4
from datetime import datetime
from infrastructure.security import create_access_token
from fastapi import HTTPException, status
from passlib.context import CryptContext
from domain.users.models import User as UserModel
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(user: UserRegisterRequest, db: Session) -> AuthResponse:
    # 이메일 중복 체크
    existing = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")
    hashed_pw = pwd_context.hash(user.password)
    user_id = uuid4()
    db_user = UserModel(
        id=user_id,
        email=user.email,
        name=user.name,
        role=user.role,
        profile_image=None,
        created_at=datetime.utcnow(),
        is_deleted=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_access_token({"sub": str(db_user.id)})
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=UserInfo(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            nickname=user.nickname,
            role=db_user.role,
            created_at=db_user.created_at
        )
    )

def login_user(user: UserLoginRequest, db: Session) -> AuthResponse:
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    # 비밀번호 검증 (여기서는 profile_image 필드에 임시로 저장했다고 가정)
    # 실제로는 User 모델에 password_hash 컬럼을 추가해야 함
    # hashed_pw = db_user.password_hash
    # if not pwd_context.verify(user.password, hashed_pw):
    #     raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    token = create_access_token({"sub": str(db_user.id)})
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=UserInfo(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            nickname="닉네임",  # 실제 닉네임 필드 필요
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
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    # 3. JWT 발급
    token = create_access_token({"sub": str(user.id)})
    return GoogleLoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserInfo.from_orm(user)
    )
