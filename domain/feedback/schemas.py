from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List

class FeedbackCreate(BaseModel):
    content: str
    category: str = "general"
    priority: str = "medium"

class FeedbackRead(BaseModel):
    id: int
    user_id: UUID
    content: str
    category: str
    priority: str
    created_at: datetime
    status: str
    class Config:
        from_attributes = True

class FeedbackList(BaseModel):
    feedbacks: List[FeedbackRead]
