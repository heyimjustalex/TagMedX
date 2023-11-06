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
        return self.task_repository.get_task_by_id(task_id)
