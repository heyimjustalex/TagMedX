from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...users.schemas.user_schema import UserListResponse, UserResponse
from ..services.group_service import GroupService
from repositories.group_repository import Roles
from features.users.services.user_service import UserService
from connectionDB.session import get_db
from features.authorization.services.token_service import TokenService, UserData
from ..schemas.group_schema import (
    GroupResposne,
    GroupCreate,
    GroupUpdate,
    MembershipCreate,
    GroupWithRoleResponse,
    GroupJoin,
    AdminGroupResponse,
)

router = APIRouter()


@router.post("/api/groups/create", tags=["Groups"], response_model=AdminGroupResponse)
def create_group(
    group_create: GroupCreate,
    db: Session = Depends(get_db),
    user_data: UserData = Depends(TokenService.get_user_data),
):
    creator_user_id = user_data.id
    group_service = GroupService(db)
    group = group_service.create_group(group_create, creator_user_id)
    role = group_service.get_role_in_group(creator_user_id, group.id)
    return AdminGroupResponse(
        name=group.name,
        description=group.description,
        id=group.id,
        role=role,
        connection_string=group.connection_string,
    )


@router.get("/api/groups", tags=["Groups"], response_model=List[GroupWithRoleResponse])
def get_groups(
    db: Session = Depends(get_db),
    user_data: UserData = Depends(TokenService.get_user_data),
):
    group_service = GroupService(db)
    user_id = user_data.id
    groups = group_service.get_groups(user_id)

    groups_with_roles = []
    for group in groups:
        role = group_service.get_role_in_group(user_id, group.id)
        group_with_role = GroupWithRoleResponse(
            name=group.name, description=group.description, id=group.id, role=role
        )
        groups_with_roles.append(group_with_role)

    return groups_with_roles


@router.get(
    "/api/groups/{group_id}",
    tags=["Groups"],
    response_model=GroupWithRoleResponse | AdminGroupResponse,
)
def get_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    db: Session = Depends(get_db),
):
    group_service = GroupService(db)
    group = group_service.get_group(group_id)
    role = group_service.get_role_in_group(user_data.id, group.id)
    if role == Roles.ADMIN:
        return AdminGroupResponse(
            name=group.name,
            description=group.description,
            id=group.id,
            role=role,
            connection_string=group.connection_string,
        )

    return GroupWithRoleResponse(
        name=group.name, description=group.description, id=group.id, role=role
    )


@router.put("/api/groups/{group_id}", tags=["Groups"], response_model=GroupResposne)
def update_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    group: GroupUpdate,
    db: Session = Depends(get_db),
):
    group_service = GroupService(db)
    group_service.check_if_admin(user_data.id, group_id)
    updated_group = group_service.update_group(group_id, group)
    return GroupResposne(
        name=updated_group.name,
        description=updated_group.description,
        id=updated_group.id,
    )


@router.delete("/api/groups/{group_id}", tags=["Groups"], response_model=GroupResposne)
def delete_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    db: Session = Depends(get_db),
):
    group_service = GroupService(db)
    group_service.check_if_admin(user_data.id, group_id)
    deleted_group = group_service.delete_group(group_id)
    return GroupResposne(
        name=deleted_group.name,
        description=deleted_group.description,
        id=deleted_group.id,
    )


@router.post(
    "/api/groups/{group_id}/add-user/{user_id}",
    tags=["Groups"],
    response_model=GroupResposne,
)
def add_user_to_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
):
    group_service = GroupService(db)
    group_service.check_if_admin(user_data.id, group_id)
    group = group_service.get_group(group_id)
    user_service = UserService(db)
    user_service.get_user(user_id)
    membership_service = GroupService(db)
    membership_data = MembershipCreate(id_user=user_id, id_group=group_id, role=role)
    membership_service.add_membership(membership_data)

    return group


@router.delete(
    "/api/groups/{group_id}/remove-user/{user_id}",
    tags=["Groups"],
    response_model=GroupResposne,
)
def remove_user_from_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    group_service = GroupService(db)
    group_service.check_if_admin(user_data.id, group_id)
    removed_group = group_service.remove_user_from_group(group_id, user_id)
    return removed_group


@router.get(
    "/api/groups/{group_id}/users", tags=["Groups"], response_model=UserListResponse
)
def get_users_in_group(group_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(db)
    group_service.get_group(group_id)
    users = group_service.get_users_in_group(group_id)
    response = UserListResponse(users=[])
    for user in users:
        response.users.append(
            UserResponse(user_id=user.id, name=user.name, surname=user.surname)
        )
    return response


@router.post("/api/groups/join", tags=["Groups"], response_model=GroupWithRoleResponse)
def join_group(
    group_join: GroupJoin,
    db: Session = Depends(get_db),
    user_data: UserData = Depends(TokenService.get_user_data),
):
    group_service = GroupService(db)
    user_id = user_data.id
    group = group_service.join_group(group_join.connection_string, user_id)
    role = group_service.get_role_in_group(user_id, group.id)
    return GroupWithRoleResponse(
        name=group.name, description=group.description, id=group.id, role=role
    )
