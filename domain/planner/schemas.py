from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date

class DailyPlannerRequest(BaseModel):
    plan_date: date  # YYYY-MM-DD
    content_count: Optional[int] = 1
    platforms: Optional[List[str]] = ["youtube"]
    content_types: Optional[List[str]] = ["video"]

class DailyPlannerResponse(BaseModel):
    plan_date: date
    tasks: List[str]
    estimated_duration: int
    priority_order: List[str]

class DailyPlanCreate(BaseModel):
    plan_date: date  # YYYY-MM-DD
    tasks: List[str]

class DailyPlanRead(BaseModel):
    id: UUID
    user_id: UUID
    plan_date: date
    tasks: List[str]
    created_at: datetime
    class Config:
        from_attributes = True

class DailyPlanList(BaseModel):
    plans: List[DailyPlanRead]
