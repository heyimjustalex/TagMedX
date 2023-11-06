from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connectionDB.session import get_db
from ..schemas.task_schema import TaskCreate, TaskResponse, TaskSchema, TaskUpdateSchema
from features.authorization.services.token_service import TokenService, UserData
from ..services.task_service import TaskService

router = APIRouter()


@router.post("/api/tasks/create", tags=["Task"], response_model=TaskResponse)
def create_task(
        task_data: TaskCreate,
        db: Session = Depends(get_db),
        user_data: UserData = Depends(TokenService.get_user_data),
):
    task_service = TaskService(db)
    current_user_id = user_data.id
    task = task_service.create_task_with_permission_check(task_data, current_user_id)
    return task


@router.get("/api/tasks", tags=["Task"], response_model=List[TaskSchema])
def get_tasks(db: Session = Depends(get_db), user_data: UserData = Depends(TokenService.get_user_data)):
    task_service = TaskService(db)
    user_id = user_data.id
    tasks = task_service.get_user_tasks(user_id)
    return tasks


@router.get("/api/tasks/{task_id}", tags=["Task"], response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task = task_service.get_task_by_id(task_id)
    return task


@router.put("/update_task/{task_id}", tags=["Task"], response_model=TaskResponse)
async def update_task(
        task_id: int,
        task_data: TaskUpdateSchema,
        db: Session = Depends(get_db),
):
    task_service = TaskService(db)
    task = task_service.update_task(task_id, task_data.dict())
    return task


@router.delete("/delete_task/{task_id}", tags=["Task"], response_model=TaskResponse)
async def delete_task(
        task_id: int,
        db: Session = Depends(get_db),
):
    task_service = TaskService(db)
    task = task_service.delete_task(task_id)
    return task
