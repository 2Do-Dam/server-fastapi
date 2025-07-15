from fastapi import APIRouter, Depends
from domain.hashtags.schemas import HashtagRecommendRequest, HashtagRecommendResponse
from domain.hashtags.services import recommend_hashtags
from infrastructure.database import get_db
from infrastructure.security import get_current_user
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/recommend", response_model=HashtagRecommendResponse)
def recommend_hashtags_api(req: HashtagRecommendRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return recommend_hashtags(req, db, user["user_id"])
