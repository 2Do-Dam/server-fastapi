from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, ARRAY
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from datetime import datetime
from core.base import Base

class DailyPlan(Base):
    __tablename__ = "daily_plans"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    plan_date = Column(String, nullable=False)  # YYYY-MM-DD
    tasks = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.utcnow)
