from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from datetime import datetime
from core.base import Base

class Content(Base):
    __tablename__ = "contents"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    upload_time = Column(DateTime, default=datetime.utcnow)
    hashtags = Column(ARRAY(String), nullable=True)
    is_published = Column(Boolean, default=False)
