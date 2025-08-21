from sqlalchemy.orm import Session
from domain.contents.models import Content
from domain.contents.schemas import ContentCreate
from typing import List, Optional
from uuid import UUID

class ContentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_contents(self) -> List[Content]:
        """모든 콘텐츠 조회"""
        return self.db.query(Content).all()
    
    def get_content_by_id(self, content_id: UUID) -> Optional[Content]:
        """ID로 콘텐츠 조회"""
        return self.db.query(Content).filter(Content.id == content_id).first()
    
    def get_contents_by_user_id(self, user_id: UUID) -> List[Content]:
        """사용자 ID로 콘텐츠 조회"""
        return self.db.query(Content).filter(Content.user_id == user_id).all()
    
    def create_content(self, content_data: ContentCreate, user_id: UUID) -> Content:
        """새 콘텐츠 생성"""
        db_content = Content(
            user_id=user_id,
            title=content_data.title,
            description=content_data.description,
            hashtags=content_data.hashtags,
            is_published=content_data.is_published
        )
        
        self.db.add(db_content)
        self.db.commit()
        self.db.refresh(db_content)
        return db_content
    
    def update_content(self, content_id: UUID, content_data: ContentCreate, user_id: UUID) -> Optional[Content]:
        """콘텐츠 업데이트"""
        content = self.db.query(Content).filter(
            Content.id == content_id, 
            Content.user_id == user_id
        ).first()
        
        if content:
            content.title = content_data.title
            content.description = content_data.description
            content.hashtags = content_data.hashtags
            content.is_published = content_data.is_published
            
            self.db.commit()
            self.db.refresh(content)
        
        return content
    
    def delete_content(self, content_id: UUID, user_id: UUID) -> bool:
        """콘텐츠 삭제"""
        content = self.db.query(Content).filter(
            Content.id == content_id, 
            Content.user_id == user_id
        ).first()
        
        if content:
            self.db.delete(content)
            self.db.commit()
            return True
        
        return False
