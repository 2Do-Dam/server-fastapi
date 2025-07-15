from domain.users.schemas import User, UserCreate
from uuid import uuid4
from datetime import datetime
from typing import List
from domain.users.models import UserRole
from sqlalchemy.orm import Session

def list_users() -> List[User]:
    return [User(
        id=uuid4(),
        email="test@example.com",
        name="테스트",
        role="youtuber",
        profile_image=None,
        created_at=datetime.utcnow(),
        is_deleted=False
    )]

def create_user(user: UserCreate) -> User:
    return User(
        id=uuid4(),
        email=user.email,
        name=user.name,
        role=user.role,
        profile_image=None,
        created_at=datetime.utcnow(),
        is_deleted=False
    )

def update_user_roles(user_id: str, roles: list[str], db: Session):
    db.query(UserRole).filter(UserRole.user_id == user_id).delete()
    for role in roles:
        db.add(UserRole(user_id=user_id, role=role))
    db.commit()
