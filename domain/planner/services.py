from domain.planner.models import DailyPlan
from domain.planner.schemas import DailyPlanCreate, DailyPlanRead
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from typing import List

def list_daily_plans(user_id: str, db: Session) -> List[DailyPlanRead]:
    plans = db.query(DailyPlan).filter(DailyPlan.user_id == user_id).all()
    return [DailyPlanRead.from_orm(plan) for plan in plans]

def create_daily_plan(user_id: str, data: DailyPlanCreate, db: Session) -> DailyPlanRead:
    plan = DailyPlan(
        id=uuid4(),
        user_id=user_id,
        plan_date=data.plan_date,
        tasks=data.tasks,
        created_at=datetime.utcnow()
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return DailyPlanRead.from_orm(plan)
