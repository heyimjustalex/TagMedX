from typing import List
from sqlalchemy.orm import Session
from models.models import Label, Membership, Group, Set


class LabelRepository:
    def __init__(self, db: Session):
        self.db = db

    def can_create_label(self, user_id, set_id) -> bool:
        groups = (
            self.db.query(Group)
            .join(Membership, Group.id == Membership.id_group)
            .filter(Membership.id_user == user_id, Membership.role == "Admin")
            .all()
        )

        group_ids = [group.id for group in groups]
        set = self.db.query(Set).filter(Set.id == set_id).first()
        if not set or set.id_group not in group_ids:
            return False

        return True

    def create_label(self, user_id, label_data) -> Label | None:
        if not self.can_create_label(user_id, label_data.id_set):
            return None

        label = Label(**label_data.dict())
        self.db.add(label)
        self.db.commit()
        self.db.refresh(label)
        return label

    def get_labels_for_set(self, set_id: int) -> List[Label]:
        return self.db.query(Label).filter(Label.id_set == set_id).all()
