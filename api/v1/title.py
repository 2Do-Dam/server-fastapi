from fastapi import APIRouter, Depends
from domain.title.schemas import TitleAnalyzeRequest, TitleAnalyzeResponse
from domain.title.services import analyze_title
from infrastructure.database import get_db
from infrastructure.security import get_current_user
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/analyze", response_model=TitleAnalyzeResponse)
def analyze_title_api(req: TitleAnalyzeRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return analyze_title(req, db, user["user_id"])
