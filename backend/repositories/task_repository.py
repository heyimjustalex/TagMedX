from sqlalchemy.orm import Session
from models.models import Task, Membership, Group, Label, Sample
from features.tasks.schemas.task_schema import TaskCreate
from .group_repository import Roles


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def is_user_admin_in_group(self, user_id: int, group_id: int):
        membership = (
            self.db.query(Membership)
            .filter(Membership.id_user == user_id)
            .filter(Membership.id_group == group_id)
            .filter(Membership.role == Roles.ADMIN)
            .first()
        )
        return membership is not None

    def create_task(self, task_data: TaskCreate) -> Task:
        task = Task(**task_data.dict())
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task_by_id(self, task_id):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_user_tasks(self, user_id: int):
        groups = (
            self.db.query(Group)
            .join(Membership, Group.id == Membership.id_group)
            .filter(Membership.id_user == user_id)
            .all()
        )

        group_ids = [group.id for group in groups]

        tasks = (
            self.db.query(Task)
            .filter(Task.id_group.in_(group_ids))
            .all()
        )

        task_data = [
            {"max_samples_for_user": task.max_samples_for_user, "name": task.name, "description": task.description,
             "type": task.type} for task in tasks]

        return task_data

    def update_task(self, task_id: int, new_task_data):
        task = self.get_task_by_id(task_id)
        if task:
            for key, value in new_task_data.items():
                setattr(task, key, value)
            self.db.commit()
        return task

    def delete_task(self, task_id: int):
        db_task = self.get_task_by_id(task_id)
        if db_task:
            self.db.query(Label).filter(Label.id_task == task_id).delete(
                synchronize_session=False
            )
            self.db.query(Sample).filter(Sample.id_task == task_id).delete(
                synchronize_session=False
            )
            self.db.delete(db_task)
            self.db.commit()
        return db_task
