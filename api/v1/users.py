from fastapi import APIRouter
from domain.users.schemas import User, UserCreate
from typing import List
from domain.users.services import list_users, create_user
from domain.users.schemas import UserRoleUpdateRequest
from domain.users.services import update_user_roles
from infrastructure.database import get_db
from infrastructure.security import get_current_user
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import BackgroundTasks
from infrastructure.database import get_redis
import random, time
import smtplib
from email.mime.text import MIMEText
from core.config import settings
from pydantic import BaseModel, EmailStr
from domain.auth.schemas import UserProfileUpdateRequest, UserRegisterRequest, UserInfo, AuthResponse
from domain.auth.services import update_user_profile, create_verified_user, create_access_token

# 이메일 전송 함수
EMAIL_SENDER = settings.EMAIL_SENDER  
EMAIL_APP_PASSWORD = settings.EMAIL_APP_PASSWORD
def send_email(to_email, code):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(EMAIL_SENDER, EMAIL_APP_PASSWORD)
    msg = MIMEText(f'인증코드: {code}')
    msg['Subject'] = '이메일 인증코드'
    msg['To'] = to_email
    msg['From'] = EMAIL_SENDER
    smtp.sendmail(EMAIL_SENDER, to_email, msg.as_string())
    smtp.quit()

router = APIRouter()

@router.get("/", response_model=List[User])
def list_users_api():
    return list_users()

@router.post("/", response_model=User)
def create_user_api(user: UserCreate):
    return create_user(user)

@router.post("/roles")
def set_roles(req: UserRoleUpdateRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    update_user_roles(user["user_id"], req.roles, db)
    return {"message": "역할이 저장되었습니다."}

class EmailRequest(BaseModel):
    email: EmailStr

@router.post("/send-email-code")
def send_email_code(req: EmailRequest, background_tasks: BackgroundTasks, redis=Depends(get_redis)):
    email = req.email
    code = str(random.randint(1000, 9999))
    expires = 300  # 5분
    redis.setex(f"email_code:{email}", expires, code)
    background_tasks.add_task(send_email, email, code)
    return {"msg": "인증코드가 전송되었습니다."}

# 회원가입: 이메일, 비밀번호만 받고 DB에는 저장하지 않음
@router.post("/register")
def register(user: UserRegisterRequest, redis=Depends(get_redis)):
    # 이메일 중복 체크 (임시로 redis에 저장)
    if redis.get(f"pending_user:{user.email}"):
        return {"msg": "이미 인증 대기 중인 이메일입니다.", "success": False}
    redis.setex(f"pending_user:{user.email}", 600, user.password)  # 10분간 임시 저장
    return {"msg": "이메일 인증을 진행하세요.", "success": True}

class EmailVerifyRequest(BaseModel):
    email: EmailStr
    code: str

# 이메일 인증 성공 시 DB에 저장 및 access_token 발급
@router.post("/verify-email-code", response_model=AuthResponse)
def verify_email_code(req: EmailVerifyRequest, redis=Depends(get_redis), db: Session = Depends(get_db)):
    email = req.email
    code = req.code
    saved_code = redis.get(f"email_code:{email}")
    if not saved_code:
        return {"msg": "인증코드가 만료되었거나 없습니다.", "success": False}
    if saved_code != code:
        return {"msg": "인증코드가 일치하지 않습니다.", "success": False}
    # 임시 저장된 회원가입 정보 확인
    password = redis.get(f"pending_user:{email}")
    if not password:
        return {"msg": "회원가입 정보가 만료되었습니다.", "success": False}
    # DB에 사용자 저장 및 access_token 발급
    user = create_verified_user(email, password, db)
    token = create_access_token({"sub": str(user.id)})
    redis.delete(f"email_code:{email}")
    redis.delete(f"pending_user:{email}")
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=UserInfo(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )
    )

@router.put("/profile")
def update_profile(req: UserProfileUpdateRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    updated = update_user_profile(user["user_id"], req, db)
    return {"message": "프로필이 업데이트되었습니다.", "user": {
        "id": str(updated.id),
        "email": updated.email,
        "name": updated.name,
        "nickname": updated.nickname,
        "role": updated.role
    }}
