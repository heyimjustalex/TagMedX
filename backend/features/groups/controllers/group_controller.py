from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.group_schema import Group, GroupCreate, GroupUpdate, MembershipCreate, User
from ..services.group_service import GroupService
from features.users.services.user_service import UserService
from connectionDB.session import get_db

router = APIRouter()


@router.post("/api/groups/{id_user}/create", tags=["Groups"], response_model=Group)
def create_group(id_user: int, group: GroupCreate, db: Session = Depends(get_db)):
    group_service = GroupService(db)  # here should be returned the current user who wants to create the group
    return group_service.create_group(group, id_user)


@router.get("/api/groups", tags=["Groups"], response_model=List[Group])
def get_groups(db: Session = Depends(get_db)):
    group_service = GroupService(db)
    return group_service.get_groups()


@router.get("/api/groups/{group_id}", tags=["Groups"], response_model=Group)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    group = group_service.get_group(group_id)
    return group


@router.put("/api/groups/{group_id}", tags=["Groups"], response_model=Group)
def update_group(group_id: int, group: GroupUpdate, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    updated_group = group_service.update_group(group_id, group)
    return updated_group


@router.delete("/api/groups/{group_id}", tags=["Groups"], response_model=Group)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    deleted_group = group_service.delete_group(group_id)
    return deleted_group


@router.post("/api/groups/{group_id}/add-user/{user_id}", tags=["Groups"], response_model=Group)
def add_user_to_group(group_id: int, user_id: int, role: str, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    group = group_service.get_group(group_id)
    user_service = UserService(db)
    user_service.get_user(user_id)
    membership_service = GroupService(db)
    membership_data = MembershipCreate(id_user=user_id, id_group=group_id, role=role)
    membership_service.add_membership(membership_data)

    return group


@router.delete("/api/groups/{group_id}/remove-user/{user_id}", tags=["Groups"], response_model=Group)
def remove_user_from_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    removed_group = group_service.remove_user_from_group(group_id, user_id)
    return removed_group


@router.get("/api/groups/{group_id}/users", tags=["Groups"], response_model=List[User])
def get_users_in_group(group_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    group_service.get_group(group_id)
    users = group_service.get_users_in_group(group_id)
    return users


@router.post("/api/groups/{group_name}/join", tags=["Groups"], response_model=Group)
def join_group(group_name: str, connection_string: str, user_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    user_service = UserService(db)  # here should be returned the current user who wants to join the group
    user_service.get_user(user_id)
    group = group_service.join_group(group_name, user_id, connection_string)
    return group
