from sqlalchemy.orm import Session
from models.models import Set, Membership, Group, Label, Sample, Package
from features.sets.schemas.set_schema import SetCreate
from .group_repository import Roles


class SetRepository:
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

    def create_set(self, set_data: SetCreate) -> Set:
        set = Set(**set_data.dict())
        self.db.add(set)
        self.db.commit()
        self.db.refresh(set)
        return set

    def get_set_by_id(self, set_id):
        return self.db.query(Set).filter(Set.id == set_id).first()

    def get_user_sets(self, user_id: int):
        groups = (
            self.db.query(Group)
            .join(Membership, Group.id == Membership.id_group)
            .filter(Membership.id_user == user_id)
            .all()
        )

        group_ids = [group.id for group in groups]

        sets = self.db.query(Set).filter(Set.id_group.in_(group_ids)).all()

        set_data = [
            {  # "max_samples_for_user": set.max_samples_for_user,
                "name": set.name,
                "description": set.description,
                "type": set.type,
            }
            for set in sets
        ]

        return set_data

    def update_set(self, set_id: int, new_set_data):
        set = self.get_set_by_id(set_id)
        if set:
            for key, value in new_set_data.items():
                setattr(set, key, value)
            self.db.commit()
        return set

    def delete_set(self, set_id: int):
        db_set = self.get_set_by_id(set_id)
        if db_set:
            self.db.query(Label).filter(Label.id_set == set_id).delete(
                synchronize_session=False
            )
            self.db.query(Sample).filter(
                Sample.Package.has(Package.id_set == set_id)
            ).delete(synchronize_session=False)
            self.db.delete(db_set)
            self.db.commit()
        return db_set
