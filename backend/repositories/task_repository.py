from sqlalchemy.orm import Session
from models.models import Task, Membership
from features.tasks.schemas.task_schema import TaskCreate, TaskResponse


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def is_user_admin_in_group(self, user_id: int, group_id: int):
        membership = (
            self.db.query(Membership)
            .filter(Membership.id_user == user_id)
            .filter(Membership.id_group == group_id)
            .filter(Membership.role == "Admin")
            .first()
        )
        return membership is not None

    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        task = Task(**task_data.dict())
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task_by_id(self, task_id):
        return self.db.query(Task).filter(Task.id == task_id).first()
