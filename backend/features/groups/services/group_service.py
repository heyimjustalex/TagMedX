from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas.group_schema import GroupCreate, GroupUpdate, MembershipCreate
from features.exceptions.definitions.definitions import *
from repositories.group_repository import GroupRepository


class GroupService:
    def __init__(self, db: Session):
        self.db = db
        self.group_repository = GroupRepository(db)

    def create_group(self, group: GroupCreate, creator_user_id: int):
        group = self.group_repository.create_group(group, creator_user_id)
        return group

    def get_groups(self, user_id):
        return self.group_repository.get_groups(user_id)

    def get_role_in_group(self, user_id, group_id):
        return self.group_repository.get_role_in_group(user_id, group_id)

    def get_group(self, group_id: int):
        group = self.group_repository.get_group(group_id)
        if not group:
            raise GroupNotFoundException(status_code=404, detail="Group not found")
        return group

    def get_users_in_group(self, group_id: int):
        users = self.group_repository.get_users_in_group(group_id)
        if not users:
            raise UserNotFoundException(status_code=404, detail="No users found in the group")
        return users

    def update_group(self, group_id: int, group: GroupUpdate):
        updated_group = self.group_repository.update_group(group_id, group)
        if not updated_group:
            raise GroupNotFoundException(status_code=404, detail="Group not found")
        return updated_group

    def delete_group(self, group_id: int):
        deleted_group = self.group_repository.delete_group(group_id)
        if not deleted_group:
            raise GroupNotFoundException(status_code=404, detail="Group not found")
        return deleted_group

    def add_membership(self, membership_data: MembershipCreate):
        try:
            return self.group_repository.add_membership(membership_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to add membership")

    def remove_user_from_group(self, group_id: int, user_id: int):
        removed_group = self.group_repository.remove_user_from_group(group_id, user_id)
        if not removed_group:
            raise GroupNotFoundException(status_code=404, detail="Group not found")
        return removed_group

    def join_group(self, connection_string: str, user_id: int):
        group = self.group_repository.get_group_by_connection_string(connection_string)
        if not group:
            raise GroupNotFoundException(status_code=404, detail="Group not found")

        membership_data = MembershipCreate(id_user=user_id, id_group=group.id, role="User")
        self.add_membership(membership_data)
        return group
