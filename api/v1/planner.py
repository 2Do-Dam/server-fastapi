from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from domain.planner.schemas import DailyPlanCreate, DailyPlanRead, DailyPlanList
from domain.planner.services import list_daily_plans, create_daily_plan
from infrastructure.database import get_db
from infrastructure.security import get_current_user

router = APIRouter()

@router.get("/", response_model=DailyPlanList)
def get_daily_plans(db: Session = Depends(get_db), user=Depends(get_current_user)):
    plans = list_daily_plans(user["user_id"], db)
    return {"plans": plans}

@router.post("/", response_model=DailyPlanRead)
def create_daily_plan_api(data: DailyPlanCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_daily_plan(user["user_id"], data, db)
