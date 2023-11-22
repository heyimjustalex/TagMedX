import secrets
import string
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from features.exceptions.definitions.definitions import *
from repositories.group_repository import GroupRepository
from repositories.membership_repository import MembershipRepository
from models.models import Group, Membership
from repositories.group_repository import Roles
from typing import List


class GroupService:
    def __init__(self, db: Session):
        self.group_repository = GroupRepository(db)
        self.membership_repository = MembershipRepository(db)

    def create_group(self, group_name: str, creator_user_id: int) -> Group:
        characters = string.ascii_letters + string.digits

        group = Group()
        group.name = group_name
        group.connection_string = "".join(secrets.choice(characters) for _ in range(32))

        self.group_repository.create_group(group)

        membership = Membership()
        membership.id_group = group.id
        membership.id_user = creator_user_id
        membership.role = Roles.ADMIN

        self.membership_repository.create_membership(membership)

        return group

    def get_user_groups(self, user_id: int) -> List[Group]:
        return self.group_repository.get_groups_by_user(user_id)

    def get_role_in_group(self, user_id: int, group_id: int) -> str:
        membership = self.get_membership(group_id, user_id)
        return membership.role

    def get_group(self, group_id: int) -> Group:
        group = self.group_repository.get_group_by_id(group_id)
        if not group:
            raise GroupNotFoundException(status_code=404, detail="Group not found")
        return group

    def update_group(
        self,
        group_id: int,
        name: str | None = None,
        description: str | None = None,
        connection_string: str | None = None,
    ) -> Group:
        group = self.get_group(group_id)

        if name:
            group.name = name

        if description:
            group.description = description

        if connection_string:
            group.connection_string = connection_string

        self.group_repository.update()
        return group

    def delete_group(self, group_id: int) -> Group:
        group = self.get_group(group_id)
        self.group_repository.delete_group(group)
        return group

    def remove_user_from_group(self, group_id: int, user_id: int) -> Group:
        group = self.get_group(group_id)
        membership = self.get_membership(group_id, user_id)
        self.membership_repository.delete_membership(membership)
        return group

    def get_membership(self, id_group: int, id_user: int) -> Membership:
        membership = self.membership_repository.get_membership(id_user, id_group)
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found in group.",
            )
        return membership

    def get_group_by_connection_string(self, connection_string: str) -> Group:
        group = self.group_repository.get_group_by_connection_string(connection_string)
        if not group:
            raise GroupNotFoundException(status_code=404, detail="Group not found")
        return group

    def join_group(self, connection_string: str, user_id: int) -> Group:
        group = self.get_group_by_connection_string(connection_string)

        membership = Membership()
        membership.id_group = group.id
        membership.id_user = user_id
        membership.role = Roles.USER

        self.membership_repository.create_membership(membership)
        return group

    def check_if_admin(self, id_user: int, id_group: int) -> str:
        role = self.get_role_in_group(id_user, id_group)
        if role != Roles.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No authority to perform this operation.",
            )
        return role
