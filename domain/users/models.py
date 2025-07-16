from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from datetime import datetime
from core.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    nickname = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)
    role = Column(String, default="youtuber")
    profile_image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

class UserRole(Base):
    __tablename__ = "user_roles"
    user_id = Column(PG_UUID(as_uuid=True), primary_key=True)
    role = Column(String, primary_key=True)
