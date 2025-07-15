from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from domain.feedback.schemas import FeedbackCreate, FeedbackRead, FeedbackList
from domain.feedback.services import list_feedbacks, create_feedback
from infrastructure.database import get_db
from infrastructure.security import get_current_user

router = APIRouter()

@router.get("/", response_model=FeedbackList)
def get_feedbacks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    feedbacks = list_feedbacks(user["user_id"], db)
    return {"feedbacks": feedbacks}

@router.post("/", response_model=FeedbackRead)
def create_feedback_api(data: FeedbackCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_feedback(user["user_id"], data, db)
