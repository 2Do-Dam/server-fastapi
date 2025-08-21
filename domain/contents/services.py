from domain.contents.schemas import Content, ContentCreate
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from repository.content_repository import ContentRepository
from fastapi import HTTPException

def list_contents(db: Session) -> List[Content]:
    """모든 콘텐츠 목록 조회"""
    content_repo = ContentRepository(db)
    contents = content_repo.get_all_contents()
    return [Content.model_validate(content) for content in contents]

def create_content(content: ContentCreate, user_id: UUID, db: Session) -> Content:
    """새 콘텐츠 생성"""
    content_repo = ContentRepository(db)
    db_content = content_repo.create_content(content, user_id)
    return Content.model_validate(db_content)

def get_content_by_id(content_id: UUID, db: Session) -> Optional[Content]:
    """ID로 콘텐츠 조회"""
    content_repo = ContentRepository(db)
    content = content_repo.get_content_by_id(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다.")
    return Content.model_validate(content)

def get_contents_by_user_id(user_id: UUID, db: Session) -> List[Content]:
    """사용자 ID로 콘텐츠 조회"""
    content_repo = ContentRepository(db)
    contents = content_repo.get_contents_by_user_id(user_id)
    return [Content.model_validate(content) for content in contents]

def update_content(content_id: UUID, content: ContentCreate, user_id: UUID, db: Session) -> Content:
    """콘텐츠 업데이트"""
    content_repo = ContentRepository(db)
    updated_content = content_repo.update_content(content_id, content, user_id)
    if not updated_content:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다.")
    return Content.model_validate(updated_content)

def delete_content(content_id: UUID, user_id: UUID, db: Session) -> bool:
    """콘텐츠 삭제"""
    content_repo = ContentRepository(db)
    success = content_repo.delete_content(content_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다.")
    return success
