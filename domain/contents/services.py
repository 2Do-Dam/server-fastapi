from domain.contents.schemas import Content, ContentCreate
from uuid import uuid4
from datetime import datetime
from typing import List

def list_contents() -> List[Content]:
    return [Content(
        id=uuid4(),
        user_id=uuid4(),
        title="테스트 콘텐츠",
        description="설명",
        upload_time=datetime.utcnow(),
        hashtags=["#test"],
        is_published=True
    )]

def create_content(content: ContentCreate) -> Content:
    return Content(
        id=uuid4(),
        user_id=uuid4(),
        title=content.title,
        description=content.description,
        upload_time=datetime.utcnow(),
        hashtags=content.hashtags,
        is_published=content.is_published or False
    )
