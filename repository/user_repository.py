from sqlalchemy.orm import Session
from domain.users.models import User, UserRole
from domain.users.schemas import UserCreate
from typing import List, Optional
from uuid import UUID
import bcrypt

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_users(self) -> List[User]:
        """모든 사용자 조회 (삭제되지 않은 사용자만)"""
        return self.db.query(User).filter(User.is_deleted == False).all()
    
    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """ID로 사용자 조회"""
        return self.db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """이메일로 사용자 조회"""
        return self.db.query(User).filter(User.email == email, User.is_deleted == False).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        """새 사용자 생성"""
        # 비밀번호 해싱
        password_hash = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        db_user = User(
            email=user_data.email,
            name=user_data.name,
            nickname=user_data.nickname,
            password_hash=password_hash,
            role=user_data.role,
            profile_image=user_data.profile_image
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user_profile(self, user_id: UUID, name: str, nickname: str, role: str) -> Optional[User]:
        """사용자 프로필 업데이트"""
        user = self.get_user_by_id(user_id)
        if user:
            user.name = name
            user.nickname = nickname
            user.role = role
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def delete_user(self, user_id: UUID) -> bool:
        """사용자 삭제 (소프트 삭제)"""
        user = self.get_user_by_id(user_id)
        if user:
            user.is_deleted = True
            self.db.commit()
            return True
        return False
    
    def get_user_roles(self, user_id: UUID) -> List[UserRole]:
        """사용자의 역할 목록 조회"""
        return self.db.query(UserRole).filter(UserRole.user_id == user_id).all()
    
    def update_user_roles(self, user_id: UUID, roles: List[str]) -> bool:
        """사용자 역할 업데이트"""
        try:
            # 기존 역할 삭제
            self.db.query(UserRole).filter(UserRole.user_id == user_id).delete()
            
            # 새 역할 추가
            for role in roles:
                user_role = UserRole(user_id=user_id, role=role)
                self.db.add(user_role)
            
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False
