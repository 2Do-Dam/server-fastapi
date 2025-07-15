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
