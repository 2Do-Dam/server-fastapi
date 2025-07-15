from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from domain.calendar.schemas import CalendarTaskCreate, CalendarTaskUpdate, CalendarTaskRead, CalendarTaskList, CalendarRecommendRequest, CalendarRecommendResponse
from domain.calendar.services import list_calendar_tasks, create_calendar_task, update_calendar_task, delete_calendar_task, recommend_calendar_task
from infrastructure.database import get_db
from infrastructure.security import get_current_user
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=CalendarTaskList)
def get_calendar_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    tasks = list_calendar_tasks(user["user_id"], db)
    return {"tasks": tasks}

@router.post("/", response_model=CalendarTaskRead)
def create_calendar_task_api(data: CalendarTaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_calendar_task(user["user_id"], data, db)

@router.put("/{task_id}", response_model=CalendarTaskRead)
def update_calendar_task_api(task_id: UUID, data: CalendarTaskUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return update_calendar_task(user["user_id"], str(task_id), data, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{task_id}")
def delete_calendar_task_api(task_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return delete_calendar_task(user["user_id"], str(task_id), db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/recommend", response_model=CalendarRecommendResponse)
def recommend_calendar_task_api(req: CalendarRecommendRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return recommend_calendar_task(user["user_id"], req, db)
