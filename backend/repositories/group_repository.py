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

    def update(self):
        self.db.commit()

    def delete_group(self, group: Group):
        self.db.delete(group)
        self.db.commit()

    def get_group_by_id(self, group_id: int) -> Group | None:
        return self.db.query(Group).filter(Group.id == group_id).first()

    def get_groups_by_user(self, id_user) -> List[Group]:
        return (
            self.db.query(Group)
            .filter(Group.Membership.any(Membership.id_user == id_user))
            .all()
        )

    def get_group_by_connection_string(self, connection_string: str) -> Group | None:
        return (
            self.db.query(Group)
            .filter(Group.connection_string == connection_string)
            .first()
        )
