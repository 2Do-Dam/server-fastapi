from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from datetime import datetime
from core.base import Base

class HashtagSearch(Base):
    __tablename__ = "hashtag_searches"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    keywords = Column(String)
    result = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
