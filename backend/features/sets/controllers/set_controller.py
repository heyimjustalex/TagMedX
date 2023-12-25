from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from connectionDB.session import get_db
from ..schemas.set_schema import SetCreate, SetResponse, SetUpdate
from features.authorization.services.token_service import TokenService, UserData
from ..services.set_service import SetService
from ...groups.services.group_service import GroupService

router = APIRouter()


@router.post("/api/sets", tags=["Sets"], response_model=SetResponse)
def create_set(
    set_create: SetCreate,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, set_create.id_group)

    set_service = SetService(db)
    set = set_service.create_set(
        set_create.id_group,
        set_create.package_size,
        set_create.name,
        set_create.description,
        set_create.type,
    )

    return SetResponse(
        id=set.id,
        id_group=set.id_group,
        package_size=set.package_size,
        name=set.name,
        description=set.description,
        type=set.type,
    )


@router.get(
    "/api/sets/group/{id_group}", tags=["Sets"], response_model=list[SetResponse]
)
def get_sets_in_group(
    id_group: int,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    group_service = GroupService(db)
    _ = group_service.get_membership(id_group, user_data.id)

    set_service = SetService(db)
    sets = set_service.get_sets_in_group(id_group)

    response: list[SetResponse] = []
    for set in sets:
        response.append(
            SetResponse(
                id=set.id,
                id_group=set.id_group,
                package_size=set.package_size,
                name=set.name,
                description=set.description,
                type=set.type,
            )
        )

    return response


@router.get("/api/sets/{id_set}", tags=["Sets"], response_model=SetResponse)
def get_set(
    id_set: int,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    set_service = SetService(db)
    set = set_service.get_set(id_set)

    group_service = GroupService(db)
    _ = group_service.get_membership(set.id_group, user_data.id)

    return SetResponse(
        id=set.id,
        id_group=set.id_group,
        package_size=set.package_size,
        name=set.name,
        description=set.description,
        type=set.type,
    )


@router.put("/api/sets/{id_set}", tags=["Sets"], response_model=SetResponse)
async def update_set(
    id_set: int,
    set_update: SetUpdate,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    set_service = SetService(db)
    set = set_service.get_set(id_set)

    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, set.id_group)

    set = set_service.update_set(
        set.id, set_update.name, set_update.description, set_update.type
    )

    return SetResponse(
        id=set.id,
        id_group=set.id_group,
        package_size=set.package_size,
        name=set.name,
        description=set.description,
        type=set.type,
    )


@router.delete("/api/sets/{id_set}", tags=["Sets"])
async def delete_set(
    id_set: int,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    set_service = SetService(db)
    set = set_service.get_set(id_set)

    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, set.id_group)

    set_service.delete_set(set.id)

    return {"message": "Set removed successfully"}
