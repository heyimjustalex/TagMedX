import secrets
import string
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models import Group, User, Membership, Task
from typing import List
from features.groups.schemas.group_schema import (
    GroupCreate,
    GroupUpdate,
    MembershipCreate,
)


class Roles:
    ADMIN = "Admin"
    USER = "User"


class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_group(self, group: GroupCreate, creator_user_id: int) -> Group:
        max_group_id = self.db.query(func.max(Group.id)).scalar() or 0
        new_group_id = max_group_id + 1

        characters = string.ascii_letters + string.digits
        connection_string = "".join(secrets.choice(characters) for i in range(10))

        db_group = Group(
            id=new_group_id, connection_string=connection_string, name=group.name
        )
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)

        membership_data = MembershipCreate(
            id_user=creator_user_id, id_group=db_group.id, role=Roles.ADMIN
        )
        self.add_membership(membership_data)

        return db_group

    def get_group_by_name(self, group_name: str) -> Group | None:
        return self.db.query(Group).filter(Group.name == group_name).first()

    def get_groups(self, user_id) -> List[Group]:
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

    def get_role_in_group(self, user_id: int, group_id: int) -> str | None:
        membership = (
            self.db.query(Membership)
            .filter_by(id_user=user_id, id_group=group_id)
            .first()
        )
        if not membership:
            return None
        return membership.role

    def get_group(self, group_id: int) -> Group | None:
        return self.db.query(Group).filter(Group.id == group_id).first()

    def get_users_in_group(self, group_id: int) -> List[User]:
        memberships = (
            self.db.query(Membership.id_user)
            .filter(Membership.id_group == group_id)
            .all()
        )
        user_ids = [membership.id_user for membership in memberships]

        users = self.db.query(User).filter(User.id.in_(user_ids)).all()
        return users

    def update_group(self, group_id: int, group: GroupUpdate) -> Group | None:
        db_group = self.get_group(group_id)
        if db_group:
            for key, value in group.dict().items():
                setattr(db_group, key, value)
            self.db.commit()
            self.db.refresh(db_group)
        return db_group

    def delete_group(self, group_id: int) -> Group | None:
        db_group = self.get_group(group_id)
        if db_group:
            self.db.query(Task).filter(Task.id_group == group_id).delete(
                synchronize_session=False
            )
            self.db.query(Membership).filter(Membership.id_group == group_id).delete(
                synchronize_session=False
            )
            self.db.delete(db_group)
            self.db.commit()
        return db_group

    def add_membership(self, membership_data: MembershipCreate) -> Membership:
        membership = Membership(**membership_data.dict())
        self.db.add(membership)
        self.db.commit()
        self.db.refresh(membership)
        return membership

    def remove_user_from_group(self, group_id: int, user_id: int) -> Group | None:
        membership = (
            self.db.query(Membership)
            .filter(Membership.id_user == user_id, Membership.id_group == group_id)
            .first()
        )
        if membership:
            self.db.delete(membership)
            self.db.commit()
        return self.get_group(group_id)
