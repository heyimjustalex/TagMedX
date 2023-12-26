from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..services.group_service import GroupService
from repositories.group_repository import Roles
from features.users.services.user_service import UserService
from ...sets.services.set_service import SetService
from ...packages.services.package_service import PackageService
from ...samples.services.sample_service import SampleService
from ...examination.services.examination_service import ExaminationService
from connectionDB.session import get_db
from features.authorization.services.token_service import TokenService, UserData
from ..schemas.group_schema import (
    GroupCreate,
    GroupUpdate,
    GroupWithRoleResponse,
    GroupJoin,
    AdminGroupResponse,
    GroupMemberResponse,
    GroupStatsResponse,
)

router = APIRouter()


@router.post("/api/groups/create", tags=["Groups"], response_model=AdminGroupResponse)
def create_group(
    group_create: GroupCreate,
    db: Annotated[Session, Depends(get_db)],
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
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
    db: Annotated[Session, Depends(get_db)],
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
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
    db: Annotated[Session, Depends(get_db)],
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
    "/api/groups/{group_id}/stats",
    tags=["Groups"],
    response_model=GroupStatsResponse,
)
def get_group_stats(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    group_service = GroupService(db)
    set_service = SetService(db)
    package_service = PackageService(db)
    sample_service = SampleService(db)
    examination_service = ExaminationService(db)

    group = group_service.get_group(group_id)
    role = group_service.get_role_in_group(user_data.id, group.id)

    return GroupStatsResponse(
        name=group.name,
        description=group.description,
        id=group.id,
        role=role,
        sets=set_service.count_sets_in_group(group.id),
        detection_sets=set_service.count_sets_in_group(group.id, "Detection"),
        classification_sets=set_service.count_sets_in_group(group.id, "Classification"),
        packages=package_service.count_packages_in_group(group.id),
        ready_packages=package_service.count_packages_in_group(group.id, is_ready=True),
        user_packages=package_service.count_packages_in_group(
            group.id, id_user=user_data.id
        ),
        user_ready_packages=package_service.count_packages_in_group(
            group.id, id_user=user_data.id, is_ready=True
        ),
        samples=sample_service.count_samples_in_group(group.id),
        examinated_samples=sample_service.count_samples_in_group(
            group.id, examinated=True
        ),
        user_samples=sample_service.count_samples_in_group(
            group.id, id_user=user_data.id
        ),
        user_examinated_samples=sample_service.count_samples_in_group(
            group.id, id_user=user_data.id, examinated=True
        ),
        tentative_examinations=examination_service.count_examinations_in_group(
            group.id, tentative=True
        ),
        user_tentative_examinations=examination_service.count_examinations_in_group(
            group.id, id_user=user_data.id, tentative=True
        ),
    )


@router.get("/api/groups/{group_id}/name", tags=["Groups"], response_model=str)
def get_group_name(
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
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
    db: Annotated[Session, Depends(get_db)],
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


@router.delete("/api/groups/{group_id}", tags=["Groups"])
def delete_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, group_id)
    group_service.delete_group(group_id)
    return {"message": "Group removed successfully"}


@router.delete(
    "/api/groups/{group_id}/user/{user_id}",
    tags=["Groups"],
)
def remove_user_from_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, group_id)
    group_service.remove_user_from_group(group_id, user_id)
    return {"message": "User successfully removed from the group"}


@router.get(
    "/api/groups/{group_id}/users",
    tags=["Groups"],
    response_model=list[GroupMemberResponse],
)
def get_users_in_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    group_service = GroupService(db)
    _ = group_service.get_membership(group_id, user_data.id)

    user_service = UserService(db)
    users = user_service.get_users_in_group(group_id)

    response: list[GroupMemberResponse] = []
    for user in users:
        role = group_service.get_role_in_group(user.id, group_id)
        response.append(
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
    db: Annotated[Session, Depends(get_db)],
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
):
    group_service = GroupService(db)
    user_id = user_data.id
    group = group_service.join_group(group_join.connection_string, user_id)
    role = group_service.get_role_in_group(user_id, group.id)
    return GroupWithRoleResponse(
        name=group.name, description=group.description, id=group.id, role=role
    )


@router.get("/api/groups/{group_id}/role", tags=["Groups"], response_model=str)
def get_role_in_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    group_service = GroupService(db)
    _ = group_service.get_group(group_id)
    role = group_service.get_role_in_group(user_data.id, group_id)
    return role
