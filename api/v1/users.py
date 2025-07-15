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

# 이메일 전송 함수
EMAIL_SENDER = settings.EMAIL_SENDER  # 실제 이메일로 변경 필요
EMAIL_APP_PASSWORD = settings.EMAIL_APP_PASSWORD  # 실제 앱 비밀번호로 변경 필요
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

class EmailVerifyRequest(BaseModel):
    email: EmailStr
    code: str

@router.post("/verify-email-code")
def verify_email_code(req: EmailVerifyRequest, redis=Depends(get_redis)):
    email = req.email
    code = req.code
    saved_code = redis.get(f"email_code:{email}")
    if not saved_code:
        return {"msg": "인증코드가 만료되었거나 없습니다.", "success": False}
    if saved_code != code:
        return {"msg": "인증코드가 일치하지 않습니다.", "success": False}
    redis.delete(f"email_code:{email}")
    return {"msg": "이메일 인증 성공", "success": True}
