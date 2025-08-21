from fastapi import APIRouter, Depends
from domain.contents.schemas import ContentCreate, Content
from typing import List
from domain.contents.services import list_contents, create_content
from infrastructure.database import get_db
from infrastructure.security import get_current_user
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/", response_model=List[Content])
def list_contents_api(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return list_contents(db, current_user["user_id"])

@router.post("/", response_model=Content)
def create_content_api(content: ContentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_content(content, current_user["user_id"], db)
