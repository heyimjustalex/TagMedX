from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connectionDB.session import get_db
from ..schemas.task_schema import TaskCreate, TaskResponse
from features.authorization.services.token_service import TokenService, UserData
from ..services.task_service import TaskService

router = APIRouter()


@router.post("/api/tasks/", tags=["Task"], response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    user_data: UserData = Depends(TokenService.get_user_data),
):
    task_service = TaskService(db)
    current_user_id = user_data.id
    task = task_service.create_task_with_permission_check(task_data, current_user_id)
    return task


@router.get("/api/tasks/{task_id}", tags=["Task"], response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task = task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
