from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class ContentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    hashtags: Optional[List[str]] = None
    is_published: Optional[bool] = False

class Content(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    upload_time: datetime
    hashtags: Optional[List[str]] = None
    is_published: bool

    class Config:
        from_attributes = True
