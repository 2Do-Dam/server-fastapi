from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from domain.users.schemas import User, UserCreate, UserRoleUpdateRequest, UserProfileUpdateRequest
from domain.users.services import list_users, create_user, update_user_roles
from domain.auth.schemas import UserRegisterRequest, UserInfo, AuthResponse
from domain.auth.services import update_user_profile, create_verified_user, create_access_token
from infrastructure.database import get_db, get_redis
from infrastructure.security import get_current_user
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from core.config import settings
from typing import List
import random, time
import smtplib
from email.mime.text import MIMEText

def send_email(to_email, code):
    """이메일 전송 함수"""
    try:
        # 환경변수를 함수 내에서 직접 가져오기
        email_sender = settings.EMAIL_SENDER
        email_password = settings.EMAIL_APP_PASSWORD
        
        print("=== 이메일 전송 디버깅 시작 ===")
        print(f"EMAIL_SENDER: {email_sender}")
        print(f"EMAIL_APP_PASSWORD 길이: {len(email_password) if email_password else 0}")
        print(f"수신자: {to_email}")
        print(f"인증코드: {code}")
        
        # 환경변수 확인
        if not email_sender or not email_password:
            print(f"❌ 이메일 설정 오류: EMAIL_SENDER={email_sender}, EMAIL_APP_PASSWORD={'설정됨' if email_password else '설정되지 않음'}")
            return False
            
        print(f"✅ 환경변수 확인 완료")
        print(f"📧 이메일 전송 시도: {to_email}")
        print(f"👤 발신자: {email_sender}")
        
        # SMTP 연결
        print("🔌 SMTP 연결 시도...")
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        print("✅ SMTP 연결 성공")
        
        print("🔒 STARTTLS 시작...")
        smtp.starttls()
        print("✅ STARTTLS 완료")
        
        # 로그인 시도
        print("🔑 Gmail 로그인 시도...")
        smtp.login(email_sender, email_password)
        print(f"✅ Gmail 로그인 성공: {email_sender}")
        
        # 이메일 메시지 생성
        print("📝 이메일 메시지 생성...")
        msg = MIMEText(f'인증코드: {code}')
        msg['Subject'] = '이메일 인증코드'
        msg['To'] = to_email
        msg['From'] = email_sender
        print("✅ 이메일 메시지 생성 완료")
        
        # 이메일 전송
        print("📤 이메일 전송 시도...")
        smtp.sendmail(email_sender, to_email, msg.as_string())
        print(f"✅ 이메일 전송 성공: {to_email}")
        
        smtp.quit()
        print("✅ SMTP 연결 종료")
        print("=== 이메일 전송 완료 ===")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Gmail 인증 실패: {e}")
        print("💡 앱 비밀번호가 올바른지 확인하세요.")
        print("💡 2단계 인증이 활성화되어 있고 앱 비밀번호가 생성되었는지 확인하세요.")
        print("💡 Gmail 계정 보안 설정을 확인하세요.")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"❌ SMTP 연결 실패: {e}")
        print("💡 네트워크 연결이나 방화벽 설정을 확인하세요.")
        print("💡 포트 587이 차단되어 있을 수 있습니다.")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP 오류: {e}")
        print(f"💡 오류 코드: {getattr(e, 'smtp_code', 'N/A')}")
        print(f"💡 오류 메시지: {getattr(e, 'smtp_error', 'N/A')}")
        return False
    except Exception as e:
        print(f"❌ 이메일 전송 중 예상치 못한 오류: {e}")
        print(f"💡 오류 타입: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

router = APIRouter()

@router.get("/", response_model=List[User])
def list_users_api(db: Session = Depends(get_db)):
    return list_users(db)

@router.post("/", response_model=User)
def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

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
    
    print(f"=== 이메일 인증코드 전송 API 시작 ===")
    print(f"📧 요청된 이메일: {email}")
    print(f"🔢 생성된 인증코드: {code}")
    print(f"⏰ 만료 시간: {expires}초")
    
    try:
        # Redis에 인증코드 저장
        print("💾 Redis에 인증코드 저장 시도...")
        redis.setex(f"email_code:{email}", expires, code)
        print(f"✅ Redis에 인증코드 저장 완료: {email} -> {code}")
        
        # 동기적으로 이메일 전송 시도 (테스트용)
        print("📤 이메일 전송 함수 호출...")
        email_sent = send_email(email, code)
        
        if email_sent:
            print("✅ 이메일 전송 성공 - 응답 반환")
            return {
                "msg": "인증코드가 전송되었습니다.",
                "success": True,
                "email": email,
                "expires_in": expires,
                "code": code  # 개발 환경에서만 표시
            }
        else:
            # 이메일 전송 실패 시 Redis에서 코드 삭제
            print("❌ 이메일 전송 실패 - Redis에서 코드 삭제")
            redis.delete(f"email_code:{email}")
            return {
                "msg": "이메일 전송에 실패했습니다. 설정을 확인해주세요.",
                "success": False,
                "error": "이메일 전송 실패"
            }
        
    except Exception as e:
        print(f"❌ 인증코드 저장/전송 중 예외 발생: {e}")
        print(f"💡 예외 타입: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        # 오류 발생 시 Redis에서 코드 삭제 시도
        try:
            redis.delete(f"email_code:{email}")
            print("✅ Redis에서 인증코드 삭제 완료")
        except Exception as del_e:
            print(f"❌ Redis에서 인증코드 삭제 실패: {del_e}")
        
        return {
            "msg": "인증코드 전송에 실패했습니다. 잠시 후 다시 시도해주세요.",
            "success": False,
            "error": str(e)
        }

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
    
    try:
        # 인증코드 확인
        saved_code = redis.get(f"email_code:{email}")
        if not saved_code:
            raise HTTPException(status_code=400, detail="인증코드가 만료되었거나 없습니다.")
        
        # Redis 데이터 타입 확인 및 변환
        if isinstance(saved_code, bytes):
            saved_code = saved_code.decode('utf-8')
        elif isinstance(saved_code, str):
            saved_code = saved_code
        else:
            saved_code = str(saved_code)
        
        print(f"저장된 인증코드: {saved_code}, 입력된 코드: {code}")
        
        if saved_code != code:
            raise HTTPException(status_code=400, detail="인증코드가 일치하지 않습니다.")
        
        # 임시 저장된 회원가입 정보 확인
        password = redis.get(f"pending_user:{email}")
        if not password:
            raise HTTPException(status_code=400, detail="회원가입 정보가 만료되었습니다.")
        
        # Redis 데이터 타입 확인 및 변환
        if isinstance(password, bytes):
            password = password.decode('utf-8')
        elif isinstance(password, str):
            password = password
        else:
            password = str(password)
        
        print(f"저장된 비밀번호: {password[:3]}***")
        
        # DB에 사용자 저장 및 access_token 발급
        user = create_verified_user(email, password, db)
        token = create_access_token({"sub": str(user.id)})
        
        # Redis에서 임시 데이터 삭제
        redis.delete(f"email_code:{email}")
        redis.delete(f"pending_user:{email}")
        
        print(f"사용자 생성 성공: {user.id}")
        
        return AuthResponse(
            access_token=token,
            token_type="bearer",
            user=UserInfo(
                id=user.id,
                email=user.email,
                name=user.name,
                nickname=user.nickname,
                role=user.role,
                created_at=user.created_at
            )
        )
        
    except HTTPException:
        # HTTPException은 그대로 전파
        raise
    except Exception as e:
        print(f"이메일 인증 중 예상치 못한 오류: {e}")
        print(f"오류 타입: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="이메일 인증 중 오류가 발생했습니다.")

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

@router.get("/debug/email-config")
def debug_email_config():
    """이메일 설정 디버깅용 (개발 환경에서만 사용)"""
    return {
        "email_sender": settings.EMAIL_SENDER if settings.EMAIL_SENDER else "설정되지 않음",
        "email_app_password": "설정됨" if settings.EMAIL_APP_PASSWORD else "설정되지 않음",
        "gmail_smtp": "smtp.gmail.com:587",
        "note": "이 엔드포인트는 개발 환경에서만 사용하세요."
    }
