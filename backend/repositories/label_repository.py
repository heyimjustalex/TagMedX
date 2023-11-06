from typing import List
from sqlalchemy.orm import Session
from models.models import Label, Membership, Group, Task
from features.label.schemas.label_schema import LabelSchema


class LabelRepository:
    def __init__(self, db: Session):
        self.db = db

    def can_create_label(self, user_id, task_id):
        groups = (
            self.db.query(Group)
            .join(Membership, Group.id == Membership.id_group)
            .filter(Membership.id_user == user_id, Membership.role == "Admin")
            .all()
        )

        group_ids = [group.id for group in groups]
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task or task.id_group not in group_ids:
            return False

        return True

    def create_label(self, user_id, label_data):
        if not self.can_create_label(user_id, label_data.id_task):
            return None

        label = Label(**label_data.dict())
        self.db.add(label)
        self.db.commit()
        self.db.refresh(label)
        return label

    def get_labels_for_task(self, task_id: int) -> List[LabelSchema]:
        return self.db.query(Label).filter(Label.id_task == task_id).all()
