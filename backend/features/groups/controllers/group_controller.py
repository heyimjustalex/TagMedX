from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.group_schema import Group, GroupCreate, GroupUpdate, MembershipCreate, User
from features.exceptions.definitions.definitions import GroupNotFoundException, UserNotFoundException
from ..services.group_service import GroupService, UserService
from connectionDB.session import get_db

router = APIRouter()


@router.post("/api/groups", response_model=Group)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    return group_service.create_group(group)


@router.get("/api/groups", response_model=List[Group])
def get_groups(db: Session = Depends(get_db)):
    group_service = GroupService(db)
    return group_service.get_groups()


@router.get("/api/groups/{group_id}", response_model=Group)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    group = group_service.get_group(group_id)
    if not group:
        raise GroupNotFoundException(status_code=404, detail="Group not found")
    return group


@router.put("/api/groups/{group_id}", response_model=Group)
def update_group(group_id: int, group: GroupUpdate, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    updated_group = group_service.update_group(group_id, group)
    if not updated_group:
        raise GroupNotFoundException(status_code=404, detail="Group not found")
    return updated_group


@router.delete("/api/groups/{group_id}", response_model=Group)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    deleted_group = group_service.delete_group(group_id)
    if not deleted_group:
        raise GroupNotFoundException(status_code=404, detail="Group not found")
    return deleted_group


@router.post("/api/groups/{group_id}/add-user/{user_id}", response_model=Group)
def add_user_to_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    group = group_service.get_group(group_id)
    if not group:
        raise GroupNotFoundException(status_code=404, detail="Group not found")

    user_service = UserService()
    user = user_service.get_user_id(db, user_id)
    if not user:
        raise UserNotFoundException(status_code=404, detail="Users not found")

    membership_service = GroupService(db)
    membership_data = MembershipCreate(id_user=user_id, id_group=group_id)
    membership_service.add_membership(db, membership_data)

    return group


@router.delete("/api/groups/{group_id}/remove-user/{user_id}", response_model=Group)
def remove_user_from_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    removed_group = group_service.remove_user_from_group(group_id, user_id)
    if not removed_group:
        raise GroupNotFoundException(status_code=404, detail="Group not found")
    return removed_group


@router.get("/api/groups/{group_id}/users", response_model=List[User])
def get_users_in_group(group_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    group = group_service.get_group(group_id)

    if not group:
        raise GroupNotFoundException(status_code=404, detail="Group not found")

    users = group_service.get_users_in_group(db, group_id)
    return users
