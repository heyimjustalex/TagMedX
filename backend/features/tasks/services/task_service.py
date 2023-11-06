from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.task_repository import TaskRepository
from ..schemas.task_schema import TaskCreate
from features.exceptions.definitions.definitions import PermissionDenied


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db)

    def create_task_with_permission_check(
        self, task_data: TaskCreate, current_user_id: int
    ):
        group_id = task_data.id_group

        if not self.task_repository.is_user_admin_in_group(current_user_id, group_id):
            raise PermissionDenied(status_code=403, detail="Permission denied")

        task = self.task_repository.create_task(task_data)
        return task

    def get_task_by_id(self, task_id):
        task = self.task_repository.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def get_user_tasks(self, user_id: int):
        return self.task_repository.get_user_tasks(user_id)

    def update_task(self, task_id: int, new_task_data):
        update_task = self.task_repository.update_task(task_id, new_task_data)
        if not update_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return update_task

    def delete_task(self, task_id: int):
        return self.task_repository.delete_task(task_id)
