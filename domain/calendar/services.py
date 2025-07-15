from domain.calendar.models import CalendarTask
from domain.calendar.schemas import CalendarTaskCreate, CalendarTaskUpdate, CalendarTaskRead, CalendarRecommendRequest, CalendarRecommendResponse
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from typing import List

def list_calendar_tasks(user_id: str, db: Session) -> List[CalendarTaskRead]:
    tasks = db.query(CalendarTask).filter(CalendarTask.user_id == user_id).all()
    return [CalendarTaskRead.from_orm(task) for task in tasks]

def create_calendar_task(user_id: str, data: CalendarTaskCreate, db: Session) -> CalendarTaskRead:
    task = CalendarTask(
        id=uuid4(),
        user_id=user_id,
        title=data.title,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time,
        status=data.status or "준비",
        created_at=datetime.utcnow()
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return CalendarTaskRead.from_orm(task)

def update_calendar_task(user_id: str, task_id: str, data: CalendarTaskUpdate, db: Session) -> CalendarTaskRead:
    task = db.query(CalendarTask).filter(CalendarTask.id == task_id, CalendarTask.user_id == user_id).first()
    if not task:
        raise Exception("일정을 찾을 수 없습니다.")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return CalendarTaskRead.from_orm(task)

def delete_calendar_task(user_id: str, task_id: str, db: Session):
    task = db.query(CalendarTask).filter(CalendarTask.id == task_id, CalendarTask.user_id == user_id).first()
    if not task:
        raise Exception("일정을 찾을 수 없습니다.")
    db.delete(task)
    db.commit()
    return {"message": "삭제되었습니다."}

def recommend_calendar_task(user_id: str, req: CalendarRecommendRequest, db: Session) -> CalendarRecommendResponse:
    # 예시: 사용자의 가장 최근 일정 이후 3일 뒤를 추천일로 반환
    last_task = db.query(CalendarTask).filter(CalendarTask.user_id == user_id).order_by(CalendarTask.end_time.desc()).first()
    from datetime import timedelta, date
    if last_task and last_task.end_time:
        base_date = last_task.end_time.date()
    else:
        base_date = date.today()
    recommended_date = (base_date + timedelta(days=3)).isoformat()
    return CalendarRecommendResponse(
        recommended_date=recommended_date,
        reason="이전 일정 이후 3일 뒤 추천",
        estimated_duration=req.duration or 60
    )
