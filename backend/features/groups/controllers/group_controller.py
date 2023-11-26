from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..services.group_service import GroupService
from repositories.group_repository import Roles
from features.users.services.user_service import UserService
from connectionDB.session import get_db
from features.authorization.services.token_service import TokenService, UserData
from ..schemas.group_schema import (
    GroupCreate,
    GroupUpdate,
    GroupWithRoleResponse,
    GroupJoin,
    AdminGroupResponse,
    GroupMemberListResponse,
    GroupMemberResponse,
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
    group = group_service.create_group(group_create.name, creator_user_id)
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
    groups = group_service.get_user_groups(user_id)

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

@router.get(
    "/api/groups/{group_id}/name",
    tags=["Groups"],
    response_model=str
)
def get_group_name(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    db: Session = Depends(get_db),
):
    group_service = GroupService(db)
    group = group_service.get_group(group_id)

    return group.name


@router.put(
    "/api/groups/{group_id}", tags=["Groups"], response_model=AdminGroupResponse
)
def update_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    group_update: GroupUpdate,
    db: Session = Depends(get_db),
):
    group_service = GroupService(db)
    role = group_service.check_if_admin(user_data.id, group_id)
    updated_group = group_service.update_group(
        group_id,
        group_update.name,
        group_update.description,
        group_update.connection_string,
    )
    return AdminGroupResponse(
        name=updated_group.name,
        description=updated_group.description,
        id=updated_group.id,
        connection_string=updated_group.connection_string,
        role=role,
    )


@router.delete(
    "/api/groups/{group_id}", tags=["Groups"], response_model=None
)
def delete_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    db: Session = Depends(get_db),
):
    group_service = GroupService(db)
    role = group_service.check_if_admin(user_data.id, group_id)
    deleted_group = group_service.delete_group(group_id)
    return None


@router.delete(
    "/api/groups/{group_id}/user/{user_id}",
    tags=["Groups"],
    response_model=None,
)
def remove_user_from_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    group_service = GroupService(db)
    role = group_service.check_if_admin(user_data.id, group_id)
    removed_group = group_service.remove_user_from_group(group_id, user_id)
    return None


@router.get(
    "/api/groups/{group_id}/users",
    tags=["Groups"],
    response_model=GroupMemberListResponse,
)
def get_users_in_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    db: Session = Depends(get_db),
):
    group_service = GroupService(db)
    _ = group_service.get_membership(group_id, user_data.id)

    user_service = UserService(db)
    users = user_service.get_users_in_group(group_id)

    response = GroupMemberListResponse(members=[])
    for user in users:
        role = group_service.get_role_in_group(user.id, group_id)
        response.members.append(
            GroupMemberResponse(
                user_id=user.id,
                e_mail=user.e_mail,
                name=user.name,
                surname=user.surname,
                title=user.title,
                specialization=user.specialization,
                practice_start_year=user.practice_start_year,
                role=role,
            )
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
