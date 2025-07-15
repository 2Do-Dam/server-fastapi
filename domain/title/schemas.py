from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class TitleAnalyzeRequest(BaseModel):
    title: str
    platform: str
    content_type: Optional[str] = "video"

class TitleAnalyzeResponse(BaseModel):
    title: str
    click_through_rate_score: float
    engagement_score: float
    suggestions: List[str]
    feedback: str
    platform_optimized: bool

class TitleAnalysisCreate(BaseModel):
    title: str
    result: str

class TitleAnalysis(BaseModel):
    id: int
    user_id: UUID
    title: str
    result: str
    created_at: datetime
    class Config:
        from_attributes = True
