from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class CalendarRecommendRequest(BaseModel):
    content_type: str
    platform: str
    duration: Optional[int] = None
    complexity: Optional[str] = "medium"

class CalendarRecommendResponse(BaseModel):
    recommended_date: str  # YYYY-MM-DD
    reason: str
    estimated_duration: int

class CalendarTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    status: Optional[str] = "준비"

class CalendarTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None

class CalendarTaskRead(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class CalendarTaskList(BaseModel):
    tasks: List[CalendarTaskRead]
