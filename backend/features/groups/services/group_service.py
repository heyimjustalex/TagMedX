from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas.group_schema import Group, GroupCreate, GroupUpdate, MembershipCreate
from features.exceptions.definitions.definitions import *
from repositories.group_repository import GroupRepository, UserRepository


class GroupService:
    def __init__(self, db: Session):
        self.db = db
        self.group_repository = GroupRepository(db)

    def create_group(self, group: GroupCreate):
        return self.group_repository.create_group(group)

    def get_groups(self):
        return self.group_repository.get_groups()

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

    def get_users_id(self, user_id: int):
        return self.group_repository.get_users_id(user_id)

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


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def get_user_id(self, user_id: int):
        return self.user_repository.get_user_id(user_id)
