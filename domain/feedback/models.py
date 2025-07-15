from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from datetime import datetime
from core.base import Base

class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    content = Column(String, nullable=False)
    category = Column(String, default="general")
    priority = Column(String, default="medium")
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")
