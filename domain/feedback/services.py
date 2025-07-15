from domain.feedback.models import Feedback
from domain.feedback.schemas import FeedbackCreate, FeedbackRead
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from typing import List

def list_feedbacks(user_id: str, db: Session) -> List[FeedbackRead]:
    feedbacks = db.query(Feedback).filter(Feedback.user_id == user_id).all()
    return [FeedbackRead.from_orm(fb) for fb in feedbacks]

def create_feedback(user_id: str, data: FeedbackCreate, db: Session) -> FeedbackRead:
    fb = Feedback(
        user_id=user_id,
        content=data.content,
        category=data.category,
        priority=data.priority,
        created_at=datetime.utcnow(),
        status="pending"
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return FeedbackRead.from_orm(fb)
