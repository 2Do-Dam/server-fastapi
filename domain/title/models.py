from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from datetime import datetime
from core.base import Base

class TitleAnalysis(Base):
    __tablename__ = "title_analyses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String)
    result = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
