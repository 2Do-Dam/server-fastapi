from domain.users.schemas import User, UserCreate, UserProfileUpdateRequest
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from repository.user_repository import UserRepository
from fastapi import HTTPException

def list_users(db: Session) -> List[User]:
    """모든 사용자 목록 조회"""
    user_repo = UserRepository(db)
    users = user_repo.get_all_users()
    return [User.model_validate(user) for user in users]

def create_user(user: UserCreate, db: Session) -> User:
    """새 사용자 생성"""
    user_repo = UserRepository(db)
    
    # 이메일 중복 체크
    existing_user = user_repo.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
    
    db_user = user_repo.create_user(user)
    return User.model_validate(db_user)

def get_user_by_id(user_id: UUID, db: Session) -> Optional[User]:
    """ID로 사용자 조회"""
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return User.model_validate(user)

def get_user_by_email(email: str, db: Session) -> Optional[User]:
    """이메일로 사용자 조회"""
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return User.from_orm(user)

def update_user_roles(user_id: UUID, roles: List[str], db: Session) -> bool:
    """사용자 역할 업데이트"""
    user_repo = UserRepository(db)
    
    # 사용자 존재 여부 확인
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    success = user_repo.update_user_roles(user_id, roles)
    if not success:
        raise HTTPException(status_code=500, detail="역할 업데이트에 실패했습니다.")
    
    return success

def update_user_profile(user_id: UUID, profile_data: UserProfileUpdateRequest, db: Session) -> User:
    """사용자 프로필 업데이트"""
    user_repo = UserRepository(db)
    
    # 사용자 존재 여부 확인
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    updated_user = user_repo.update_user_profile(
        user_id, 
        profile_data.name, 
        profile_data.nickname, 
        profile_data.role
    )
    
    if not updated_user:
        raise HTTPException(status_code=500, detail="프로필 업데이트에 실패했습니다.")
    
    return User.model_validate(updated_user)

def delete_user(user_id: UUID, db: Session) -> bool:
    """사용자 삭제 (소프트 삭제)"""
    user_repo = UserRepository(db)
    
    # 사용자 존재 여부 확인
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    success = user_repo.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=500, detail="사용자 삭제에 실패했습니다.")
    
    return success
