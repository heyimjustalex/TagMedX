from sqlalchemy.orm import Session
from models.models import Group, Membership, Set
from typing import List


class Roles:
    ADMIN = "Admin"
    USER = "User"


class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_group(self, group: Group):
        self.db.add(group)
        self.db.commit()

    def get_group_by_name(self, group_name: str) -> Group | None:
        return self.db.query(Group).filter(Group.name == group_name).first()

    def get_groups_by_user(self, user_id) -> List[Group]:
        return (
            self.db.query(Group)
            .join(Membership, Group.id == Membership.id_group)
            .filter(Membership.id_user == user_id)
            .all()
        )

    def get_group_by_connection_string(self, connection_string: str) -> Group | None:
        return (
            self.db.query(Group)
            .filter(Group.connection_string == connection_string)
            .first()
        )

    def get_membership(self, user_id: int, group_id: int) -> Membership | None:
        return (
            self.db.query(Membership)
            .filter(Membership.id_user == user_id, Membership.id_group == group_id)
            .first()
        )

    def get_group(self, group_id: int) -> Group | None:
        return self.db.query(Group).filter(Group.id == group_id).first()

    def update(self):
        self.db.commit()

    def delete_group(self, group: Group):
        self.db.query(Set).filter(Set.id_group == group.id).delete(
            synchronize_session=False
        )
        self.db.query(Membership).filter(Membership.id_group == group.id).delete(
            synchronize_session=False
        )
        self.db.delete(group)
        self.db.commit()

    def create_membership(self, membership: Membership):
        self.db.add(membership)
        self.db.commit()

    def delete_membership(self, membership: Membership):
        self.db.delete(membership)
        self.db.commit()
