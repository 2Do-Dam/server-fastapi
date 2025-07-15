from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class HashtagRecommendRequest(BaseModel):
    keywords: List[str]
    platform: Optional[str] = "youtube"
    limit: Optional[int] = 10

class HashtagRecommendResponse(BaseModel):
    hashtags: List[str]
    relevance_scores: List[float]
    platform: str

class HashtagSearchCreate(BaseModel):
    keywords: list[str]
    result: str

class HashtagSearch(BaseModel):
    id: int
    user_id: UUID
    keywords: str
    result: str
    created_at: datetime
    class Config:
        from_attributes = True
